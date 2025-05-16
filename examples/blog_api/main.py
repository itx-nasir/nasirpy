from nasirpy import App, Response, Router
from nasirpy.exceptions import NotFoundError, BadRequestError

app = App()

# Create an API router with prefix
api = Router(prefix="/api/v1")

@api.get("/users")
async def list_users(request):
    return Response({"users": ["user1", "user2"]})

@api.get("/users/{user_id}")
async def get_user(request):
    user_id = request.path_params["user_id"]
    if user_id == "0":
        raise BadRequestError("Invalid user ID")
    return Response({
        "user_id": user_id,
        "name": f"User {user_id}"
    })

@api.post("/users")
async def create_user(request):
    try:
        user_data = await request.json()
        # Validate required fields
        if "name" not in user_data:
            raise BadRequestError("name is required")
        
        return Response({
            "message": "User created",
            "user": user_data
        }, status_code=201)
    except BadRequestError as e:
        raise e
    except Exception as e:
        raise BadRequestError(str(e))

@api.post("/login")
async def login(request):
    form_data = await request.form()
    username = form_data.get("username", [""])[0]
    password = form_data.get("password", [""])[0]
    
    if not username or not password:
        raise BadRequestError("Username and password are required")
    
    return Response({
        "message": f"Logged in as {username}"
    })

# Admin routes
admin = Router(prefix="/admin")

@admin.get("/stats")
async def admin_stats(request):
    return Response({"total_users": 100})

# Include routers in the main app
app.include_router(api)
app.include_router(admin)

# Main app routes
@app.get("/")
async def hello(request):
    return Response({"message": "Hello, World!"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
