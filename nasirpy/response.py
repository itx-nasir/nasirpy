from typing import Any, Dict, Optional, Union
import json

class CaseInsensitiveDict(dict):
    """Dictionary subclass that uses lowercase keys for case-insensitive lookups."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._convert_keys()
    
    def __getitem__(self, key: str) -> str:
        return super().__getitem__(key.lower())
    
    def __setitem__(self, key: str, value: str) -> None:
        super().__setitem__(key.lower(), value)
    
    def __delitem__(self, key: str) -> None:
        super().__delitem__(key.lower())
    
    def __contains__(self, key: str) -> bool:
        return super().__contains__(key.lower())
    
    def get(self, key: str, default=None):
        return super().get(key.lower(), default)
    
    def _convert_keys(self):
        """Convert all keys to lowercase."""
        for k in list(self.keys()):
            v = super().pop(k)
            self.__setitem__(k, v)

class Response:
    def __init__(
        self,
        content: Union[str, dict, bytes],
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None
    ):
        self.status_code = status_code
        self.headers = CaseInsensitiveDict(headers or {})
        self._json = None
        
        # Handle different content types
        if isinstance(content, bytes):
            self.body = content
            if "content-type" not in self.headers:
                self.headers["content-type"] = "application/octet-stream"
        elif isinstance(content, dict):
            self._json = content  # Store JSON directly if dict
            self.body = json.dumps(content).encode()
            if "content-type" not in self.headers:
                self.headers["content-type"] = "application/json"
        else:
            self.body = str(content).encode()
            if "content-type" not in self.headers:
                self.headers["content-type"] = "text/plain"
    
    async def json(self) -> Dict:
        """Get the response content as JSON."""
        if self._json is not None:
            return self._json
        if "application/json" not in self.headers.get("content-type", "").lower():
            raise ValueError("Response content type is not JSON")
        self._json = json.loads(self.body.decode())
        return self._json

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
