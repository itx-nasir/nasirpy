import pytest
from nasirpy.response import Response
import json

@pytest.mark.asyncio
async def test_response_with_string():
    """Test Response with string content."""
    content = "Hello, World!"
    response = Response(content)
    
    assert response.status_code == 200
    assert response.body == b"Hello, World!"
    assert response.headers["content-type"] == "text/plain"

@pytest.mark.asyncio
async def test_response_with_dict():
    """Test Response with dictionary content (JSON)."""
    content = {"message": "Hello", "status": "success"}
    response = Response(content)
    
    assert response.status_code == 200
    assert json.loads(response.body.decode()) == content
    assert response.headers["content-type"] == "application/json"

@pytest.mark.asyncio
async def test_response_with_bytes():
    """Test Response with bytes content."""
    content = b"Binary data"
    response = Response(content)
    
    assert response.status_code == 200
    assert response.body == b"Binary data"
    assert response.headers["content-type"] == "application/octet-stream"

@pytest.mark.asyncio
async def test_response_with_custom_status():
    """Test Response with custom status code."""
    response = Response("Not Found", status_code=404)
    
    assert response.status_code == 404
    assert response.body == b"Not Found"
    assert response.headers["content-type"] == "text/plain"

@pytest.mark.asyncio
async def test_response_with_custom_headers():
    """Test Response with custom headers."""
    headers = {
        "X-Custom-Header": "custom-value",
        "content-type": "text/html"
    }
    response = Response("<h1>Hello</h1>", headers=headers)
    
    assert response.headers["X-Custom-Header"] == "custom-value"
    assert response.headers["content-type"] == "text/html"
    assert response.body == b"<h1>Hello</h1>"

@pytest.mark.asyncio
async def test_response_send():
    """Test Response send method."""
    response = Response({"message": "Hello"})
    
    # Mock send function to capture what was sent
    sent_messages = []
    async def mock_send(message):
        sent_messages.append(message)
    
    # Send the response
    await response.send(mock_send)
    
    # Verify the sent messages
    assert len(sent_messages) == 2
    
    # Verify response start message
    start_message = sent_messages[0]
    assert start_message["type"] == "http.response.start"
    assert start_message["status"] == 200
    assert (b"content-type", b"application/json") in start_message["headers"]
    
    # Verify response body message
    body_message = sent_messages[1]
    assert body_message["type"] == "http.response.body"
    assert json.loads(body_message["body"].decode()) == {"message": "Hello"}

@pytest.mark.asyncio
async def test_response_with_non_string_content():
    """Test Response with content that needs to be converted to string."""
    content = 42
    response = Response(content)
    
    assert response.status_code == 200
    assert response.body == b"42"
    assert response.headers["content-type"] == "text/plain"

@pytest.mark.asyncio
async def test_response_headers_case_insensitive():
    """Test that headers are case-insensitive."""
    headers = {
        "Content-Type": "application/xml",
        "X-Custom-Header": "value1"
    }
    response = Response("<xml></xml>", headers=headers)
    
    assert response.headers["content-type"] == "application/xml"
    assert response.headers["Content-Type"] == "application/xml"
    assert response.headers["X-Custom-Header"] == "value1"