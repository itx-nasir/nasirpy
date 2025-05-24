from typing import Callable, Dict, List, Optional, Tuple, Union
from .response import Response

class Router:
    def __init__(self, prefix: str = ""):
        self.prefix = prefix
        self.routes: List[Tuple[str, Dict[str, Callable]]] = []
        self.middleware: List[Callable] = []

    def route(self, path: str, methods: List[str] = ["GET"]):
        """Route decorator for registering handlers"""
        full_path = f"{self.prefix}{path}"
        
        def decorator(handler: Callable):
            method_dict = {method.upper(): handler for method in methods}
            self.routes.append((full_path, method_dict))
            return handler
        return decorator

    def get(self, path: str):
        return self.route(path, methods=["GET"])
        
    def post(self, path: str):
        return self.route(path, methods=["POST"])
        
    def put(self, path: str):
        return self.route(path, methods=["PUT"])
        
    def delete(self, path: str):
        return self.route(path, methods=["DELETE"])
        
    def patch(self, path: str):
        return self.route(path, methods=["PATCH"])
        
    def options(self, path: str):
        return self.route(path, methods=["OPTIONS"])
    
    def add_middleware(self, middleware: Callable) -> None:
        """Add middleware to this router"""
        self.middleware.append(middleware)
    
    def include_router(self, router: "Router", prefix: str = "") -> None:
        """Include another router with optional prefix"""
        combined_prefix = f"{self.prefix}{prefix}{router.prefix}"
        
        # Add all routes from the included router with the combined prefix
        for route_path, methods in router.routes:
            # Remove the router's prefix and add our combined prefix
            path_without_prefix = route_path[len(router.prefix):]
            new_path = f"{combined_prefix}{path_without_prefix}"
            self.routes.append((new_path, methods))
        
        # Add middleware from included router
        self.middleware.extend(router.middleware)
