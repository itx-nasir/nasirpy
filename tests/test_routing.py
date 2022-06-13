import pytest
from nasirpy.utils import parse_route_pattern, match_route
from nasirpy import App, Response

@pytest.mark.asyncio
async def test_dynamic_routing():
    app = App()
    
    @app.get("/users/{id}")
    async def get_user(request):
        return Response({"id": request.path_params["id"]})
    
    # Test pattern parsing
    pattern, params = parse_route_pattern("/users/{id}")
    assert params == ["id"]
    
    # Test parameter matching
    params = match_route("/users/{id}", "/users/123")
    assert params == {"id": "123"}
    
    # Test multiple parameters
    params = match_route("/users/{user_id}/posts/{post_id}", "/users/123/posts/456")
    assert params == {"user_id": "123", "post_id": "456"}
