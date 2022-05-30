from typing import Callable, Dict, List, Optional, Union, Tuple
from .request import Request
from .response import Response
from .utils import match_route

class App:
    def __init__(self):
        self.routes: List[Tuple[str, Dict[str, Callable]]] = []
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
        handler, params = self._get_handler(request.path, request.method)
        if handler is None:
            return Response({"error": "Not Found"}, status_code=404)
            
        try:
            # Add path parameters to request
            request.path_params = params or {}
            
            # Run through middleware chain
            for middleware in self.middleware:
                request = await middleware(request)
                
            response = await handler(request)
            return response
        except Exception as e:
            return Response({"error": str(e)}, status_code=500)
    
    def _get_handler(self, path: str, method: str) -> Tuple[Optional[Callable], Optional[Dict[str, str]]]:
        """
        Get the handler function and extracted parameters for a given path and method
        """
        for route_pattern, methods in self.routes:
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
