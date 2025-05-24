from typing import Callable, List, Optional, Union, Dict, Any
from abc import ABC, abstractmethod
import time
import logging
from datetime import datetime
from .request import Request
from .response import Response


class BaseMiddleware(ABC):
    """Base middleware class that all middleware should inherit from"""
    
    @abstractmethod
    async def __call__(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request and call the next middleware/handler
        
        Args:
            request: The incoming request
            call_next: Function to call the next middleware/handler
            
        Returns:
            Response object
        """
        pass


class MiddlewareManager:
    """Manages the middleware chain and execution order"""
    
    def __init__(self):
        self.middleware_stack: List[Union[BaseMiddleware, Callable]] = []
    
    def add_middleware(self, middleware: Union[BaseMiddleware, Callable]) -> None:
        """Add middleware to the stack"""
        self.middleware_stack.append(middleware)
    
    async def process_request(self, request: Request, handler: Callable) -> Response:
        """Process request through middleware chain"""
        if not self.middleware_stack:
            return await handler(request)
        
        # Create the middleware chain
        async def create_chain(index: int = 0):
            if index >= len(self.middleware_stack):
                # Reached the end, call the actual handler
                return await handler(request)
            
            middleware = self.middleware_stack[index]
            
            async def call_next():
                return await create_chain(index + 1)
            
            # Call middleware
            if isinstance(middleware, BaseMiddleware):
                return await middleware(request, call_next)
            else:
                # Function-based middleware
                return await middleware(request, call_next)
        
        return await create_chain()


# Built-in Middleware Classes

class CORSMiddleware(BaseMiddleware):
    """CORS (Cross-Origin Resource Sharing) middleware"""
    
    def __init__(
        self,
        allow_origins: List[str] = ["*"],
        allow_methods: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers: List[str] = ["*"],
        max_age: int = 86400
    ):
        self.allow_origins = allow_origins
        self.allow_methods = allow_methods
        self.allow_headers = allow_headers
        self.max_age = max_age
    
    async def __call__(self, request: Request, call_next: Callable) -> Response:
        # Handle preflight requests
        if request.method == "OPTIONS":
            response = Response({}, status_code=200)
        else:
            response = await call_next()
        
        # Add CORS headers
        origin = request.headers.get("origin")
        if origin and (self.allow_origins == ["*"] or origin in self.allow_origins):
            response.headers["Access-Control-Allow-Origin"] = origin
        elif self.allow_origins == ["*"]:
            response.headers["Access-Control-Allow-Origin"] = "*"
        
        response.headers["Access-Control-Allow-Methods"] = ", ".join(self.allow_methods)
        response.headers["Access-Control-Allow-Headers"] = ", ".join(self.allow_headers)
        response.headers["Access-Control-Max-Age"] = str(self.max_age)
        
        return response


class LoggingMiddleware(BaseMiddleware):
    """Request/Response logging middleware"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger("nasirpy")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    async def __call__(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Log request
        self.logger.info(
            f"📨 {request.method} {request.path} - "
            f"User-Agent: {request.headers.get('user-agent', 'Unknown')}"
        )
        
        # Process request
        response = await call_next()
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log response
        status_emoji = "✅" if response.status_code < 400 else "❌"
        self.logger.info(
            f"{status_emoji} {response.status_code} - "
            f"{request.method} {request.path} - "
            f"⏱️  {process_time:.3f}s"
        )
        
        return response


class TimingMiddleware(BaseMiddleware):
    """Adds processing time headers to responses"""
    
    async def __call__(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        response = await call_next()
        process_time = time.time() - start_time
        
        response.headers["X-Process-Time"] = f"{process_time:.3f}"
        return response


class SecurityHeadersMiddleware(BaseMiddleware):
    """Adds common security headers"""
    
    def __init__(self, custom_headers: Optional[Dict[str, str]] = None):
        self.security_headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }
        if custom_headers:
            self.security_headers.update(custom_headers)
    
    async def __call__(self, request: Request, call_next: Callable) -> Response:
        response = await call_next()
        
        # Add security headers
        for header, value in self.security_headers.items():
            response.headers[header] = value
        
        return response


class RateLimitMiddleware(BaseMiddleware):
    """Simple in-memory rate limiting middleware"""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.clients: Dict[str, List[float]] = {}
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP from request"""
        # Try different headers for real IP
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip
        
        # Fallback to scope client if available
        if hasattr(request, '_scope') and 'client' in request._scope:
            return request._scope['client'][0]
        
        return "unknown"
    
    async def __call__(self, request: Request, call_next: Callable) -> Response:
        client_ip = self._get_client_ip(request)
        current_time = time.time()
        
        # Clean old requests outside the window
        if client_ip in self.clients:
            self.clients[client_ip] = [
                req_time for req_time in self.clients[client_ip]
                if current_time - req_time < self.window_seconds
            ]
        else:
            self.clients[client_ip] = []
        
        # Check rate limit
        if len(self.clients[client_ip]) >= self.max_requests:
            from .exceptions import HTTPException
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Too many requests."
            )
        
        # Add current request
        self.clients[client_ip].append(current_time)
        
        response = await call_next()
        
        # Add rate limit headers
        remaining = max(0, self.max_requests - len(self.clients[client_ip]))
        response.headers["X-RateLimit-Limit"] = str(self.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(current_time + self.window_seconds))
        
        return response


# Convenience function middleware creators

def create_auth_middleware(auth_checker: Callable[[Request], bool]) -> Callable:
    """Create a custom authentication middleware"""
    async def auth_middleware(request: Request, call_next: Callable) -> Response:
        if not await auth_checker(request):
            from .exceptions import HTTPException
            raise HTTPException(status_code=401, detail="Authentication required")
        return await call_next()
    
    return auth_middleware


def create_custom_middleware(before_handler: Optional[Callable] = None, 
                           after_handler: Optional[Callable] = None) -> Callable:
    """Create custom middleware with before/after handlers"""
    async def custom_middleware(request: Request, call_next: Callable) -> Response:
        # Before request processing
        if before_handler:
            await before_handler(request)
        
        # Process request
        response = await call_next()
        
        # After request processing
        if after_handler:
            await after_handler(request, response)
        
        return response
    
    return custom_middleware
