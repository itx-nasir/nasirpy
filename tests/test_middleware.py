import pytest
from nasirpy.middleware import (
    BaseMiddleware, MiddlewareManager, CORSMiddleware,
    LoggingMiddleware, TimingMiddleware, SecurityHeadersMiddleware,
    RateLimitMiddleware
)
from nasirpy.request import Request
from nasirpy.response import Response
from nasirpy.exceptions import HTTPException
import logging
import time

@pytest.fixture
def mock_request():
    """Create a mock request for testing."""
    scope = {
        "method": "GET",
        "path": "/test",
        "query_string": b"",
        "headers": [(b"user-agent", b"pytest")],
    }
    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}
    return Request(scope, receive)

@pytest.fixture
def mock_handler():
    """Create a mock handler that returns a simple response."""
    async def handler(request):
        return Response({"message": "Test response"})
    return handler

@pytest.mark.asyncio
async def test_middleware_manager_empty(mock_request, mock_handler):
    """Test MiddlewareManager with no middleware."""
    manager = MiddlewareManager()
    response = await manager.process_request(mock_request, mock_handler)
    assert response.status_code == 200
    assert await response.json() == {"message": "Test response"}

@pytest.mark.asyncio
async def test_middleware_manager_single(mock_request, mock_handler):
    """Test MiddlewareManager with a single middleware."""
    class TestMiddleware(BaseMiddleware):
        async def __call__(self, request, call_next):
            response = await call_next()
            response.headers["X-Test"] = "test-value"
            return response
    
    manager = MiddlewareManager()
    manager.add_middleware(TestMiddleware())
    response = await manager.process_request(mock_request, mock_handler)
    assert response.headers["X-Test"] == "test-value"

@pytest.mark.asyncio
async def test_cors_middleware(mock_handler):
    """Test CORS middleware."""
    cors = CORSMiddleware(
        allow_origins=["http://localhost:3000"],
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
        max_age=3600
    )
    
    # Create request with Origin header
    scope = {
        "method": "OPTIONS",
        "path": "/test",
        "query_string": b"",
        "headers": [
            (b"origin", b"http://localhost:3000"),
            (b"access-control-request-method", b"POST"),
        ],
    }
    request = Request(scope, lambda: {"type": "http.request", "body": b"", "more_body": False})
    
    # Test preflight request
    response = await cors(request, mock_handler)
    
    assert response.status_code == 200
    assert response.headers["Access-Control-Allow-Origin"] == "http://localhost:3000"
    assert response.headers["Access-Control-Allow-Methods"] == "GET, POST"
    assert response.headers["Access-Control-Allow-Headers"] == "Content-Type"
    assert response.headers["Access-Control-Max-Age"] == "3600"

@pytest.mark.asyncio
async def test_logging_middleware(mock_request, mock_handler, caplog):
    """Test logging middleware with captured logs."""
    with caplog.at_level(logging.INFO):
        middleware = LoggingMiddleware()
        response = await middleware(mock_request, mock_handler)
        
        # Verify response
        assert response.status_code == 200
        
        # Check logs
        assert any("📨 GET /test" in record.message for record in caplog.records)
        assert any("✅ 200 - GET /test" in record.message for record in caplog.records)

@pytest.mark.asyncio
async def test_timing_middleware(mock_request, mock_handler):
    """Test timing middleware."""
    middleware = TimingMiddleware()
    response = await middleware(mock_request, mock_handler)
    
    assert "X-Process-Time" in response.headers
    process_time = float(response.headers["X-Process-Time"])
    assert process_time >= 0

@pytest.mark.asyncio
async def test_security_headers_middleware(mock_request, mock_handler):
    """Test security headers middleware."""
    custom_headers = {"Custom-Security-Header": "custom-value"}
    middleware = SecurityHeadersMiddleware(custom_headers)
    response = await middleware(mock_request, mock_handler)
    
    # Check default security headers
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["X-XSS-Protection"] == "1; mode=block"
    assert response.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
    
    # Check custom header
    assert response.headers["Custom-Security-Header"] == "custom-value"

@pytest.mark.asyncio
async def test_rate_limit_middleware(mock_request, mock_handler):
    """Test rate limit middleware."""
    middleware = RateLimitMiddleware(max_requests=2, window_seconds=1)
    
    # First request should succeed
    response1 = await middleware(mock_request, mock_handler)
    assert response1.status_code == 200
    assert response1.headers["X-RateLimit-Remaining"] == "1"
    
    # Second request should succeed
    response2 = await middleware(mock_request, mock_handler)
    assert response2.status_code == 200
    assert response2.headers["X-RateLimit-Remaining"] == "0"
    
    # Third request should fail
    with pytest.raises(HTTPException) as exc_info:
        await middleware(mock_request, mock_handler)
    assert exc_info.value.status_code == 429

@pytest.mark.asyncio
async def test_middleware_chain_order(mock_request, mock_handler):
    """Test that middleware executes in the correct order."""
    order = []
    
    class FirstMiddleware(BaseMiddleware):
        async def __call__(self, request, call_next):
            order.append("first_before")
            response = await call_next()
            order.append("first_after")
            return response
    
    class SecondMiddleware(BaseMiddleware):
        async def __call__(self, request, call_next):
            order.append("second_before")
            response = await call_next()
            order.append("second_after")
            return response
    
    manager = MiddlewareManager()
    manager.add_middleware(FirstMiddleware())
    manager.add_middleware(SecondMiddleware())
    
    await manager.process_request(mock_request, mock_handler)
    
    assert order == [
        "first_before",
        "second_before",
        "second_after",
        "first_after"
    ] 