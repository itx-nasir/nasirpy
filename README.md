# NasirPy

A lightweight, async-first Python web framework built for simplicity and performance.

## ✨ Features

- **Async/Await First** - Built on ASGI with full async support
- **Simple Routing** - Decorator-based routing with path parameters
- **Middleware System** - Comprehensive middleware support with built-in options
- **Router Grouping** - Organize routes with prefixes and nested routers
- **Exception Handling** - Clean error responses and custom exceptions
- **Type Hints** - Full type safety throughout the framework

## 🚀 Quick Start

```python
from nasirpy import App, Response

app = App()

@app.get("/")
async def hello(request):
    return Response({"message": "Hello, World!"})

@app.get("/users/{user_id}")
async def get_user(request):
    user_id = request.path_params["user_id"]
    return Response({"user_id": user_id, "name": f"User {user_id}"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

## 📦 Installation

```bash
pip install -r requirements.txt
```

## 🛠️ Middleware

```python
from nasirpy import App, CORSMiddleware, LoggingMiddleware, TimingMiddleware

app = App()

# Add built-in middleware
app.add_middleware(CORSMiddleware())
app.add_middleware(LoggingMiddleware())
app.add_middleware(TimingMiddleware())
```

## 🎯 Router Grouping

```python
from nasirpy import App, Router

app = App()
api = Router(prefix="/api/v1")

@api.get("/users")
async def list_users(request):
    return Response({"users": ["user1", "user2"]})

app.include_router(api)
```

## 📖 Examples

Check the `examples/` directory for a complete blog API example.

## 🧪 Testing

```bash
# Run tests
python -m pytest tests/ -v

# Run example
python examples/blog_api/main.py
```

## 📄 License

MIT License
