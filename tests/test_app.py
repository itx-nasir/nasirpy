import pytest
from nasirpy import App, Router, Response, Request, NotFoundError
from nasirpy.middleware import BaseMiddleware

@pytest.fixture
def app():
    """Create a test app instance."""
    return App()

@pytest.fixture
def mock_scope():
    """Create a mock ASGI scope."""
    return {
        "type": "http",
        "method": "GET",
        "path": "/test",
        "query_string": b"name=John&age=25",
        "headers": [
            (b"content-type", b"application/json"),
            (b"user-agent", b"pytest")
        ]
    }

@pytest.fixture
def mock_receive():
    """Create a mock ASGI receive function."""
    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}
    return receive

@pytest.fixture
def mock_send():
    """Create a mock ASGI send function that stores sent messages."""
    sent_messages = []
    async def send(message):
        sent_messages.append(message)
    send.messages = sent_messages
    return send

@pytest.mark.asyncio
async def test_app_basic_route(app, mock_scope, mock_receive, mock_send):
    """Test basic route registration and handling."""
    @app.get("/test")
    async def test_handler(request):
        return Response({"message": "Hello, World!"})

    await app.handle_request(mock_scope, mock_receive, mock_send)
    
    assert len(mock_send.messages) == 2
    assert mock_send.messages[0]["type"] == "http.response.start"
    assert mock_send.messages[0]["status"] == 200
    assert mock_send.messages[1]["type"] == "http.response.body"
    assert b'"message": "Hello, World!"' in mock_send.messages[1]["body"]

@pytest.mark.asyncio
async def test_app_route_not_found(app, mock_scope, mock_receive, mock_send):
    """Test 404 response for non-existent route."""
    mock_scope["path"] = "/nonexistent"
    await app.handle_request(mock_scope, mock_receive, mock_send)
    
    assert mock_send.messages[0]["status"] == 404
    assert b'"error": "No route found for GET /nonexistent"' in mock_send.messages[1]["body"]

@pytest.mark.asyncio
async def test_app_method_not_allowed(app, mock_scope, mock_receive, mock_send):
    """Test method not allowed response."""
    @app.get("/test")
    async def test_handler(request):
        return Response({"message": "Hello, World!"})

    mock_scope["method"] = "POST"
    await app.handle_request(mock_scope, mock_receive, mock_send)
    
    assert mock_send.messages[0]["status"] == 404
    assert b'"error": "No route found for POST /test"' in mock_send.messages[1]["body"]

@pytest.mark.asyncio
async def test_app_path_params(app, mock_scope, mock_receive, mock_send):
    """Test route with path parameters."""
    @app.get("/users/{user_id}")
    async def get_user(request):
        return Response({
            "user_id": request.path_params["user_id"]
        })

    mock_scope["path"] = "/users/123"
    await app.handle_request(mock_scope, mock_receive, mock_send)
    
    assert mock_send.messages[0]["status"] == 200
    assert b'"user_id": "123"' in mock_send.messages[1]["body"]

@pytest.mark.asyncio
async def test_app_include_router(app, mock_scope, mock_receive, mock_send):
    """Test including a router with prefix."""
    router = Router(prefix="/api")
    
    @router.get("/items")
    async def get_items(request):
        return Response({"items": []})
    
    app.include_router(router)
    
    mock_scope["path"] = "/api/items"
    await app.handle_request(mock_scope, mock_receive, mock_send)
    
    assert mock_send.messages[0]["status"] == 200
    assert b'"items": []' in mock_send.messages[1]["body"]

@pytest.mark.asyncio
async def test_app_middleware(app, mock_scope, mock_receive, mock_send):
    """Test middleware execution."""
    middleware_called = False
    
    class TestMiddleware(BaseMiddleware):
        async def __call__(self, request, call_next):
            nonlocal middleware_called
            middleware_called = True
            response = await call_next(request)
            response.headers["X-Test"] = "middleware"
            return response
    
    app.add_middleware(TestMiddleware())
    
    @app.get("/test")
    async def test_handler(request):
        return Response({"message": "test"})
    
    await app.handle_request(mock_scope, mock_receive, mock_send)
    
    assert middleware_called
    headers = dict(mock_send.messages[0]["headers"])
    
    # CaseInsensitiveDict converts all keys to lowercase
    assert headers[b"x-test"] == b"middleware"

@pytest.mark.asyncio
async def test_app_error_handling(app, mock_scope, mock_receive, mock_send):
    """Test error handling in routes."""
    @app.get("/error")
    async def error_handler(request):
        raise ValueError("Test error")
    
    mock_scope["path"] = "/error"
    await app.handle_request(mock_scope, mock_receive, mock_send)
    
    assert mock_send.messages[0]["status"] == 500
    assert b'"error": "Internal Server Error"' in mock_send.messages[1]["body"]
    assert b'"detail": "Test error"' in mock_send.messages[1]["body"]

@pytest.mark.asyncio
async def test_app_non_http_scope(app, mock_receive, mock_send):
    """Test handling of non-HTTP ASGI scopes."""
    scope = {"type": "websocket"}  # Non-HTTP scope
    await app.handle_request(scope, mock_receive, mock_send)
    assert len(mock_send.messages) == 0  # Should not send any response

@pytest.mark.asyncio
async def test_app_multiple_methods(app, mock_scope, mock_receive, mock_send):
    """Test route with multiple HTTP methods."""
    @app.route("/multi", methods=["GET", "POST"])
    async def multi_handler(request):
        return Response({
            "method": request.method
        })
    
    # Test GET
    mock_scope["method"] = "GET"
    mock_scope["path"] = "/multi"
    await app.handle_request(mock_scope, mock_receive, mock_send)
    assert b'"method": "GET"' in mock_send.messages[1]["body"]
    
    # Clear messages
    mock_send.messages.clear()
    
    # Test POST
    mock_scope["method"] = "POST"
    await app.handle_request(mock_scope, mock_receive, mock_send)
    assert b'"method": "POST"' in mock_send.messages[1]["body"] 