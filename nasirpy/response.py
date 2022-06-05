from typing import Any, Dict, Optional, Union
import json

class Response:
    def __init__(
        self,
        content: Union[str, dict, bytes],
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None
    ):
        self.status_code = status_code
        self.headers = headers or {}
        
        # Handle different content types
        if isinstance(content, bytes):
            self.body = content
            self.headers.setdefault("content-type", "application/octet-stream")
        elif isinstance(content, dict):
            self.body = json.dumps(content).encode()
            self.headers.setdefault("content-type", "application/json")
        else:
            self.body = str(content).encode()
            self.headers.setdefault("content-type", "text/plain")
    
    async def send(self, send: Any):
        await send({
            "type": "http.response.start",
            "status": self.status_code,
            "headers": [
                (k.encode(), v.encode())
                for k, v in self.headers.items()
            ]
        })
        
        await send({
            "type": "http.response.body",
            "body": self.body
        })
