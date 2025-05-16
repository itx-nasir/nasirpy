from typing import Callable, Dict, List, Optional, Tuple
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
