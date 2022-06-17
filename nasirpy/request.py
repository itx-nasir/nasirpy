from typing import Any, Dict, Optional, Union
from urllib.parse import parse_qs
import json
from .exceptions import BadRequestError

class Request:
    def __init__(self, scope: dict, receive: Any):
        self.scope = scope
        self.receive = receive
        self._body: Optional[bytes] = None
        self._json: Optional[Dict] = None
        self._form: Optional[Dict] = None
        self.path_params: Dict[str, str] = {}
        
    @property
    def method(self) -> str:
        return self.scope["method"]
        
    @property
    def path(self) -> str:
        return self.scope["path"]
        
    @property
    def query_params(self) -> Dict[str, list]:
        return parse_qs(self.scope["query_string"].decode())
        
    @property
    def headers(self) -> Dict[str, str]:
        return {
            k.decode(): v.decode()
            for k, v in self.scope["headers"]
        }
    
    @property
    def content_type(self) -> str:
        return self.headers.get('content-type', '').lower()

    async def body(self) -> bytes:
        if self._body is None:
            body = b""
            while True:
                message = await self.receive()
                body += message.get("body", b"")
                if not message.get("more_body", False):
                    break
            self._body = body
        return self._body

    async def json(self) -> Dict:
        """Parse and return JSON body"""
        if self._json is None:
            if 'application/json' not in self.content_type:
                raise BadRequestError("Content-Type must be application/json")
            try:
                body = await self.body()
                self._json = json.loads(body.decode())
            except json.JSONDecodeError:
                raise BadRequestError("Invalid JSON")
        return self._json

    async def form(self) -> Dict[str, str]:
        """Parse and return form data"""
        if self._form is None:
            if 'application/x-www-form-urlencoded' not in self.content_type:
                raise BadRequestError("Content-Type must be application/x-www-form-urlencoded")
            body = await self.body()
            self._form = parse_qs(body.decode())
        return self._form
