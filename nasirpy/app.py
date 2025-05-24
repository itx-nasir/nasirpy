from typing import Callable, Dict, List, Optional, Union, Tuple
from .request import Request
from .response import Response
from .utils import match_route
from .exceptions import HTTPException, NotFoundError
from .router import Router
from .middleware import MiddlewareManager, BaseMiddleware

class App(Router):
    def __init__(self):
        super().__init__()
        self.routers: List[Router] = []
        self.middleware_manager = MiddlewareManager()
        
    async def __call__(self, scope: dict, receive: Callable, send: Callable) -> None:
        """
        ASGI callable
        """
        await self.handle_request(scope, receive, send)
    
    async def handle_request(self, scope: dict, receive: Callable, send: Callable) -> None:
        """
        ASGI application handler
        """
        if scope["type"] != "http":
            return
            
        request = Request(scope, receive)
        response = await self._dispatch(request)
        await response.send(send)
    
    async def _dispatch(self, request: Request) -> Response:
        """
        Dispatch the request to the appropriate handler through middleware
        """
        try:
            handler, params = self._get_handler(request.path, request.method)
            if handler is None:
                raise NotFoundError(f"No route found for {request.method} {request.path}")

            # Set path parameters
            request.path_params = params or {}
            
            # Create the final handler that includes the route handler
            async def final_handler(req: Request) -> Response:
                return await handler(req)
            
            # Process through middleware chain
            response = await self.middleware_manager.process_request(request, final_handler)
            return response
            
        except HTTPException as e:
            return Response(
                {"error": e.detail},
                status_code=e.status_code
            )
        except Exception as e:
            return Response(
                {"error": "Internal Server Error", "detail": str(e)},
                status_code=500
            )
    
    def _get_handler(self, path: str, method: str) -> Tuple[Optional[Callable], Optional[Dict[str, str]]]:
        """
        Get the handler function and extracted parameters for a given path and method
        """
        # First check app routes
        for route_pattern, methods in self.routes:
            params = match_route(route_pattern, path)
            if params is not None and method in methods:
                return methods[method], params
        
        # Then check included routers
        for router in self.routers:
            for route_pattern, methods in router.routes:
                params = match_route(route_pattern, path)
                if params is not None and method in methods:
                    return methods[method], params
        
        return None, None
    
    def route(self, path: str, methods: List[str] = ["GET"]):
        """
        Route decorator for registering handlers
        """
        def decorator(handler: Callable):
            method_dict = {method.upper(): handler for method in methods}
            self.routes.append((path, method_dict))
            return handler
        return decorator
    
    # Convenience decorators for common HTTP methods
    def get(self, path: str):
        return self.route(path, methods=["GET"])
        
    def post(self, path: str):
        return self.route(path, methods=["POST"])
        
    def put(self, path: str):
        return self.route(path, methods=["PUT"])
        
    def delete(self, path: str):
        return self.route(path, methods=["DELETE"])
    
    def include_router(self, router: Router, prefix: str = ""):
        """Include a router with an optional prefix"""
        if prefix:
            router.prefix = prefix + router.prefix
        self.routers.append(router)
    
    # Middleware management methods
    def add_middleware(self, middleware: Union[BaseMiddleware, Callable]) -> None:
        """
        Add middleware to the application
        
        Args:
            middleware: Either a BaseMiddleware instance or a callable
        """
        self.middleware_manager.add_middleware(middleware)
    
    def middleware(self, middleware_class: Union[BaseMiddleware, Callable]):
        """
        Decorator for adding middleware
        
        Usage:
            @app.middleware
            class MyMiddleware(BaseMiddleware):
                async def __call__(self, request, call_next):
                    # middleware logic
                    return await call_next()
        """
        if isinstance(middleware_class, type):
            # If it's a class, instantiate it
            self.add_middleware(middleware_class())
        else:
            # If it's already an instance or function, use directly
            self.add_middleware(middleware_class)
        return middleware_class
