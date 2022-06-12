from typing import Callable, Dict, List, Optional, Union
from .request import Request
from .response import Response

class App:
    def __init__(self):
        self.routes: Dict[str, Dict[str, Callable]] = {}
        self.middleware: List[Callable] = []
        
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
        Dispatch the request to the appropriate handler
        """
        handler = self._get_handler(request.path, request.method)
        if handler is None:
            return Response({"error": "Not Found"}, status_code=404)
            
        try:
            # Run through middleware chain
            for middleware in self.middleware:
                request = await middleware(request)
                
            response = await handler(request)
            return response
        except Exception as e:
            return Response({"error": str(e)}, status_code=500)
    
    def _get_handler(self, path: str, method: str) -> Optional[Callable]:
        """
        Get the handler function for a given path and method
        """
        if path in self.routes and method in self.routes[path]:
            return self.routes[path][method]
        return None
    
    def route(self, path: str, methods: List[str] = ["GET"]):
        """
        Route decorator for registering handlers
        """
        def decorator(handler: Callable):
            if path not in self.routes:
                self.routes[path] = {}
            for method in methods:
                self.routes[path][method.upper()] = handler
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
