# 🚀 NasirPy

[![GitHub release](https://img.shields.io/github/v/release//nasirpy?include_prereleases&style=flat-square)](https://github.com/itx-nasir/nasirpy/releases)
[![License](https://img.shields.io/github/license/itx-nasir/nasirpy?style=flat-square)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue?style=flat-square)](https://www.python.org/downloads/)

> 🎓 A learning-focused Python web framework built from scratch to understand how web frameworks work under the hood.

## 🎯 Purpose

This project was created with the goal of deeply understanding:
- 🔍 How Python web frameworks work internally
- 🌐 ASGI/WSGI server implementations
- 🛠️ Request/Response lifecycle
- 🔄 Routing mechanisms
- 🧩 Middleware architecture
- 📦 Dependency injection patterns

## 💡 Educational Components

Each component is built from scratch to demonstrate core concepts:

### 1. HTTP Server Implementation
```python
# Understanding basic HTTP server mechanics
from nasirpy.server import HTTPServer

server = HTTPServer()
@server.handle_request
async def process_request(request):
    # Learn about raw HTTP request handling
    return Response({"message": "Hello, World!"})
```

### 2. Routing System
```python
# Learn how routing works internally
from nasirpy import App

app = App()

@app.get("/users/{id}")
async def get_user(id: int):
    # Understanding URL pattern matching and parameter extraction
    return {"id": id}
```

### 3. Middleware Chain
```python
# Explore middleware execution flow
class LoggingMiddleware:
    async def __call__(self, request, call_next):
        print(f"Request to: {request.url}")
        response = await call_next(request)
        print(f"Response status: {response.status_code}")
        return response
```

### 4. Request Parsing
```python
# Learn about HTTP request parsing
from nasirpy.request import Request

async def parse_body(self):
    content_type = self.headers.get("content-type")
    if content_type == "application/json":
        # Understanding body parsing mechanisms
        return await self.json()
```

## 📚 Learning Resources

This framework is accompanied by detailed explanations of:

- 📖 Core HTTP concepts
- 🔧 Python's async capabilities
- 🌐 Web server architecture
- 🔍 Request/Response patterns
- 🛠️ Framework design patterns

## 🚀 Getting Started

### Installation

Since this is a learning project, you can install it directly from GitHub:

```bash
# Install latest version from main branch
pip install git+https://github.com/itx-nasir/nasirpy.git

# Install a specific release version
pip install git+https://github.com/itx-nasir/nasirpy.git@v0.1.0

# Install in development mode (if you want to modify the code)
git clone https://github.com/itx-nasir/nasirpy.git
cd nasirpy
pip install -e .
```

### Basic Usage

```python
from nasirpy import App, Response

app = App()

@app.get("/")
async def hello_world():
    return Response({"message": "Hello, World!"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

## 📖 Understanding the Code

The codebase is extensively documented to explain key concepts:

- `server/`: Core server implementation and request handling
- `routing/`: URL pattern matching and route registration
- `middleware/`: Middleware chain implementation
- `request/`: Request parsing and validation
- `response/`: Response formatting and headers
- `types/`: Type definitions and annotations

## 🤝 Contributing

This is an educational project! Feel free to:

1. Ask questions about how things work
2. Suggest improvements to explanations
3. Add more educational examples
4. Improve documentation
5. Share your learning experience

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Support

If you found this educational project helpful, please give it a star! ⭐️

## 📫 Contact

Have questions about how something works?
- GitHub: [@itx-nasir](https://github.com/itx-nasir)
- Email: your.email@example.com

---

<p align="center">Built with 💡 for learning and understanding</p>
