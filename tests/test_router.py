import pytest
from nasirpy.router import Router
from nasirpy.request import Request
from nasirpy.response import Response

@pytest.fixture
def router():
    """Fixture to create a fresh Router instance for each test."""
    return Router()

@pytest.mark.asyncio
async def test_router_add_route():
    """Test adding routes to the router."""
    router = Router()
    
    async def test_handler(request):
        return Response(body="Test response")
    
    # Add a route using the route decorator
    router.route("/test", methods=["GET"])(test_handler)
    
    # Verify route exists
    route_exists = False
    for path, methods in router.routes:
        if path == "/test" and "GET" in methods and methods["GET"] == test_handler:
            route_exists = True
            break
    assert route_exists

@pytest.mark.asyncio
async def test_router_http_method_decorators():
    """Test the HTTP method-specific decorators."""
    router = Router()
    
    async def test_handler(request):
        return Response(body="Test response")
    
    # Test different HTTP method decorators
    router.get("/get-test")(test_handler)
    router.post("/post-test")(test_handler)
    router.put("/put-test")(test_handler)
    router.delete("/delete-test")(test_handler)
    
    # Verify routes exist with correct methods
    routes_dict = {path: methods for path, methods in router.routes}
    
    assert "/get-test" in [path for path, _ in router.routes]
    assert "/post-test" in [path for path, _ in router.routes]
    assert "/put-test" in [path for path, _ in router.routes]
    assert "/delete-test" in [path for path, _ in router.routes]

@pytest.mark.asyncio
async def test_router_with_prefix():
    """Test router with prefix."""
    router = Router(prefix="/api")
    
    async def test_handler(request):
        return Response(body="Test response")
    
    # Add a route
    router.get("/users")(test_handler)
    
    # Verify the route has the prefix
    route_exists = False
    for path, methods in router.routes:
        if path == "/api/users" and "GET" in methods and methods["GET"] == test_handler:
            route_exists = True
            break
    assert route_exists

@pytest.mark.asyncio
async def test_router_middleware():
    """Test adding middleware to router."""
    router = Router()
    
    async def test_middleware(request, next_handler):
        response = await next_handler(request)
        return response
    
    # Add middleware
    router.add_middleware(test_middleware)
    
    assert len(router.middleware) == 1
    assert router.middleware[0] == test_middleware

@pytest.mark.asyncio
async def test_include_router():
    """Test including one router in another."""
    main_router = Router(prefix="/api")
    sub_router = Router(prefix="/v1")
    
    async def test_handler(request):
        return Response(body="Test response")
    
    # Add route to sub router
    sub_router.get("/users")(test_handler)
    
    # Include sub router in main router
    main_router.include_router(sub_router)
    
    # Verify the combined route exists
    route_exists = False
    for path, methods in main_router.routes:
        if path == "/api/v1/users" and "GET" in methods and methods["GET"] == test_handler:
            route_exists = True
            break
    assert route_exists

@pytest.mark.asyncio
async def test_router_match_route():
    """Test matching routes with different HTTP methods."""
    router = Router()
    
    async def test_handler(request):
        return Response(body="Test response")
    
    # Add test routes
    router.route("/users/{id}", methods=["GET"])(test_handler)
    router.route("/users", methods=["POST"])(test_handler)
    
    # Test exact match
    handler, params = router.match_route("POST", "/users")
    assert handler == test_handler
    assert params == {}
    
    # Test parameter match
    handler, params = router.match_route("GET", "/users/123")
    assert handler == test_handler
    assert params == {"id": "123"}
    
    # Test non-existent route
    handler, params = router.match_route("GET", "/nonexistent")
    assert handler is None
    assert params == {}
    
    # Test wrong method
    handler, params = router.match_route("DELETE", "/users")
    assert handler is None
    assert params == {}

@pytest.mark.asyncio
async def test_router_dynamic_routes():
    """Test dynamic route parameters."""
    router = Router()
    
    async def test_handler(request):
        return Response(body="Test response")
    
    # Add routes with parameters
    router.route("/users/{user_id}/posts/{post_id}", methods=["GET"])(test_handler)
    
    # Test matching with multiple parameters
    handler, params = router.match_route("GET", "/users/123/posts/456")
    assert handler == test_handler
    assert params == {"user_id": "123", "post_id": "456"}
    
    # Test non-matching path
    handler, params = router.match_route("GET", "/users/123/comments/456")
    assert handler is None
    assert params == {}