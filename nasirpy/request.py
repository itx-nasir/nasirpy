from typing import Any, Dict, Optional
from urllib.parse import parse_qs

class Request:
    def __init__(self, scope: dict, receive: Any):
        self.scope = scope
        self.receive = receive
        self._body: Optional[bytes] = None
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
