import pytest
from nasirpy.request import Request
from nasirpy.exceptions import BadRequestError
import json

@pytest.fixture
def mock_scope():
    """Basic scope fixture for request tests."""
    return {
        "method": "GET",
        "path": "/test",
        "query_string": b"name=John&age=25",
        "headers": [
            (b"content-type", b"application/json"),
            (b"user-agent", b"pytest"),
        ],
    }

@pytest.fixture
def mock_receive():
    """Mock receive function that returns empty body."""
    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}
    return receive

@pytest.mark.asyncio
async def test_request_basic_properties(mock_scope, mock_receive):
    """Test basic request properties."""
    request = Request(mock_scope, mock_receive)
    
    assert request.method == "GET"
    assert request.path == "/test"
    assert request.query_params == {"name": ["John"], "age": ["25"]}
    assert request.headers["content-type"] == "application/json"
    assert request.headers["user-agent"] == "pytest"
    assert request.content_type == "application/json"

@pytest.mark.asyncio
async def test_request_json_body():
    """Test JSON body parsing."""
    json_data = {"message": "Hello, World!"}
    json_body = json.dumps(json_data).encode()
    
    async def receive():
        return {"type": "http.request", "body": json_body, "more_body": False}
    
    scope = {
        "method": "POST",
        "path": "/test",
        "query_string": b"",
        "headers": [(b"content-type", b"application/json")],
    }
    
    request = Request(scope, receive)
    assert await request.json() == json_data
    
    # Test caching
    assert request._json == json_data
    assert await request.json() == json_data  # Should use cached value

@pytest.mark.asyncio
async def test_request_form_data():
    """Test form data parsing."""
    form_data = b"name=John+Doe&email=john%40example.com"
    
    async def receive():
        return {"type": "http.request", "body": form_data, "more_body": False}
    
    scope = {
        "method": "POST",
        "path": "/test",
        "query_string": b"",
        "headers": [(b"content-type", b"application/x-www-form-urlencoded")],
    }
    
    request = Request(scope, receive)
    form = await request.form()
    assert form["name"] == ["John Doe"]
    assert form["email"] == ["john@example.com"]

@pytest.mark.asyncio
async def test_request_streaming_body():
    """Test streaming body with multiple chunks."""
    chunks = [b"Hello", b", ", b"World", b"!"]
    current_chunk = 0
    
    async def receive():
        nonlocal current_chunk
        if current_chunk < len(chunks):
            body = chunks[current_chunk]
            more_body = current_chunk < len(chunks) - 1
            current_chunk += 1
            return {"type": "http.request", "body": body, "more_body": more_body}
        return {"type": "http.request", "body": b"", "more_body": False}
    
    scope = {
        "method": "POST",
        "path": "/test",
        "query_string": b"",
        "headers": [(b"content-type", b"text/plain")],
    }
    
    request = Request(scope, receive)
    body = await request.body()
    assert body == b"Hello, World!"

@pytest.mark.asyncio
async def test_invalid_json():
    """Test invalid JSON handling."""
    async def receive():
        return {"type": "http.request", "body": b"invalid json", "more_body": False}
    
    scope = {
        "method": "POST",
        "path": "/test",
        "query_string": b"",
        "headers": [(b"content-type", b"application/json")],
    }
    
    request = Request(scope, receive)
    with pytest.raises(BadRequestError, match="Invalid JSON"):
        await request.json()

@pytest.mark.asyncio
async def test_wrong_content_type_json():
    """Test JSON parsing with wrong content type."""
    async def receive():
        return {"type": "http.request", "body": b"{}", "more_body": False}
    
    scope = {
        "method": "POST",
        "path": "/test",
        "query_string": b"",
        "headers": [(b"content-type", b"text/plain")],
    }
    
    request = Request(scope, receive)
    with pytest.raises(BadRequestError, match="Content-Type must be application/json"):
        await request.json()

@pytest.mark.asyncio
async def test_wrong_content_type_form():
    """Test form parsing with wrong content type."""
    async def receive():
        return {"type": "http.request", "body": b"name=test", "more_body": False}
    
    scope = {
        "method": "POST",
        "path": "/test",
        "query_string": b"",
        "headers": [(b"content-type", b"text/plain")],
    }
    
    request = Request(scope, receive)
    with pytest.raises(BadRequestError, match="Content-Type must be application/x-www-form-urlencoded"):
        await request.form()

@pytest.mark.asyncio
async def test_path_params():
    """Test path parameters."""
    scope = {
        "method": "GET",
        "path": "/users/123",
        "query_string": b"",
        "headers": [],
    }
    
    request = Request(scope, mock_receive)
    request.path_params = {"user_id": "123"}
    
    assert request.path_params["user_id"] == "123"