# Quick Start

Get your first NasirPy application running in under 5 minutes! This guide will walk you through creating a simple API that demonstrates the core features.

## 🎯 What We'll Build

A simple user management API with:
- Welcome endpoint
- User listing
- User creation
- Path parameters
- Error handling

## 📝 Step 1: Create Your First App

Create a new file called `app.py`:

```python
from nasirpy import App, Response, Router
from nasirpy.exceptions import NotFoundError

# Create the main application
app = App()

# Sample data
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
]

# Welcome endpoint
@app.get("/")
async def welcome():
    return Response({
        "message": "Welcome to NasirPy!",
        "endpoints": {
            "/": "This welcome message",
            "/users": "List all users",
            "/users/{id}": "Get user by ID",
            "/hello/{name}": "Personalized greeting"
        }
    })

# List users
@app.get("/users")
async def list_users():
    return Response({"users": users, "total": len(users)})

# Get user by ID
@app.get("/users/{user_id}")
async def get_user(request):
    user_id = int(request.path_params["user_id"])
    user = next((u for u in users if u["id"] == user_id), None)
    
    if not user:
        raise NotFoundError(f"User with ID {user_id} not found")
    
    return Response({"user": user})

# Personalized greeting
@app.get("/hello/{name}")
async def hello(request):
    name = request.path_params["name"]
    return Response({"message": f"Hello, {name}! 👋"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

## 🚀 Step 2: Run Your Application

Start the server:

```bash
python app.py
```

You should see output like:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

## 🧪 Step 3: Test Your API

Open your browser or use curl to test the endpoints:

### Welcome Message
```bash
curl http://127.0.0.1:8000/
```

Response:
```json
{
  "message": "Welcome to NasirPy!",
  "endpoints": {
    "/": "This welcome message",
    "/users": "List all users",
    "/users/{id}": "Get user by ID",
    "/hello/{name}": "Personalized greeting"
  }
}
```

### List Users
```bash
curl http://127.0.0.1:8000/users
```

### Get Specific User
```bash
curl http://127.0.0.1:8000/users/1
```

### Personalized Greeting
```bash
curl http://127.0.0.1:8000/hello/Developer
```

### Test Error Handling
```bash
curl http://127.0.0.1:8000/users/999
```

## 🎓 What You Just Learned

In this quick example, you've seen:

!!! success "Core Concepts Demonstrated"
    - **App Creation** - The main application instance
    - **Route Decorators** - `@app.get()` for defining endpoints
    - **Path Parameters** - `{user_id}` and `{name}` in URLs
    - **Request Object** - Accessing path parameters via `request.path_params`
    - **Response Object** - Returning JSON responses
    - **Error Handling** - Using `NotFoundError` for 404 responses

## 🔧 Adding Middleware

Let's enhance your app with middleware for logging and CORS:

```python
from nasirpy.middleware import LoggingMiddleware, CORSMiddleware

# Add middleware (order matters!)
app.add_middleware(CORSMiddleware())
app.add_middleware(LoggingMiddleware())
```

Add this after creating the `app` instance and before defining routes.

## 📊 Adding POST Endpoints

Let's add user creation:

```python
@app.post("/users")
async def create_user(request):
    user_data = await request.json()
    
    # Simple validation
    if "name" not in user_data or "email" not in user_data:
        from nasirpy.exceptions import BadRequestError
        raise BadRequestError("Name and email are required")
    
    # Create new user
    new_user = {
        "id": max([u["id"] for u in users]) + 1,
        "name": user_data["name"],
        "email": user_data["email"]
    }
    
    users.append(new_user)
    
    return Response(new_user, status_code=201)
```

Test it:
```bash
curl -X POST http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Charlie", "email": "charlie@example.com"}'
```

## 🎯 Next Steps

Congratulations! You've built your first NasirPy application. Here's what to explore next:

<div class="grid cards" markdown>

-   **[Your First App](first-app.md)**

    ---

    Build a more complete application with advanced features

-   **[Core Concepts](../concepts/architecture.md)**

    ---

    Understand how NasirPy works under the hood

-   **[API Reference](../api/app.md)**

    ---

    Explore all available classes and methods

-   **[Examples](../examples/basic-api.md)**

    ---

    See more real-world applications

</div>

## 💡 Tips for Learning

!!! tip "Understanding Framework Internals"
    As you build with NasirPy, pay attention to:
    
    - How routes are registered and matched
    - How middleware processes requests
    - How responses are formatted
    - How errors are handled
    
    This knowledge applies to all web frameworks!

!!! example "Experiment and Explore"
    Try modifying the code:
    
    - Add new endpoints
    - Create custom middleware
    - Handle different HTTP methods
    - Add request validation
    
    The best way to learn is by doing!

---

**🎉 Great job!** You've successfully created and run your first NasirPy application. The framework's educational design makes it easy to understand what's happening at each step. 