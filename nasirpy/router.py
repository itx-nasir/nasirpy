from typing import Callable, Dict, List, Optional, Tuple, Union
from .response import Response
import re

class Router:
    def __init__(self, prefix: str = ""):
        self.prefix = self._normalize_prefix(prefix)
        self.routes: List[Tuple[str, Dict[str, Callable]]] = []
        self.middleware: List[Callable] = []

    def _normalize_prefix(self, prefix: str) -> str:
        """Normalize the prefix to start with / and not end with /"""
        if not prefix:
            return ""
        prefix = "/" + prefix.strip("/")
        return prefix

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

    def _extract_params(self, route_pattern: str, path: str) -> Optional[Dict[str, str]]:
        """Extract parameters from the path based on the route pattern."""
        # Convert route pattern to regex pattern
        pattern = re.sub(r'{([^:}]+)(?::([^}]+))?}', r'(?P<\1>[^/]+)', route_pattern)
        pattern = f'^{pattern}$'
        
        # Try to match the path
        match = re.match(pattern, path)
        if match:
            return match.groupdict()
        return None

    def match_route(self, method: str, path: str) -> Tuple[Optional[Callable], Dict[str, str]]:
        """Match a path and method to a route handler and extract parameters."""
        method = method.upper()
        
        for route_path, methods in self.routes:
            # Check if the route supports the method
            if method not in methods:
                continue
                
            # Try to extract parameters
            params = self._extract_params(route_path, path)
            if params is not None:
                return methods[method], params
        
        return None, {}
