# 🚀 NasirPy Framework

<div align="center">

[![GitHub release](https://img.shields.io/github/v/release/itx-nasir/nasirpy?include_prereleases&style=flat-square)](https://github.com/itx-nasir/nasirpy/releases)
[![License](https://img.shields.io/github/license/itx-nasir/nasirpy?style=flat-square)](https://github.com/itx-nasir/nasirpy/blob/master/LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue?style=flat-square)](https://www.python.org/downloads/)

**Educational Python web framework built from scratch to understand how web frameworks work under the hood**

[Get Started](getting-started/installation.md){ .md-button .md-button--primary }
[View on GitHub](https://github.com/itx-nasir/nasirpy){ .md-button }

</div>

---

## 🎯 Purpose

NasirPy was created with the goal of deeply understanding how Python web frameworks work internally. Every component is built from scratch to demonstrate core concepts that power modern web frameworks.

!!! tip "Perfect for Learning"
    This framework is designed for developers who want to understand the internals of web frameworks like FastAPI, Flask, and Django.

## ✨ What You'll Learn

<div class="grid cards" markdown>

-   :material-web: **HTTP Server Implementation**

    ---

    Learn how web servers handle HTTP requests and responses at the protocol level.

-   :material-router: **Routing Mechanisms**

    ---

    Understand URL pattern matching, parameter extraction, and route registration.

-   :material-layers: **Middleware Architecture**

    ---

    Discover how middleware chains process requests and responses.

-   :material-sync: **ASGI/WSGI Concepts**

    ---

    Compare synchronous and asynchronous web server interfaces.

</div>

## 🚀 Quick Example

Here's how simple it is to create an API with NasirPy:

```python
from nasirpy import App, Response

app = App()

@app.get("/")
async def hello_world():
    return Response({"message": "Hello, World!"})

@app.get("/users/{user_id}")
async def get_user(request):
    user_id = request.path_params["user_id"]
    return Response({"user_id": user_id, "name": f"User {user_id}"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

## 🎓 Educational Components

### Core Features Implemented

- [x] **HTTP Server** - Built from scratch to understand request handling
- [x] **Routing System** - URL pattern matching and parameter extraction  
- [x] **Middleware Chain** - Request/response processing pipeline
- [x] **Request Parsing** - HTTP request body and header parsing
- [x] **Response Formatting** - JSON and HTML response generation
- [x] **Error Handling** - Exception management and error responses

### Learning Resources

Each component comes with detailed explanations:

- 📖 **Inline Documentation** - Every function and class is documented
- 🔍 **Code Comments** - Explaining the "why" behind implementation choices
- 📚 **Conceptual Guides** - Understanding web framework patterns
- 🧪 **Working Examples** - Real applications you can run and modify

## 🛠️ Installation

Get started in seconds:

```bash
pip install git+https://github.com/itx-nasir/nasirpy.git
```

Or for development:

```bash
git clone https://github.com/itx-nasir/nasirpy.git
cd nasirpy
pip install -e .
```

## 📖 Documentation Structure

<div class="grid cards" markdown>

-   **Getting Started**

    ---

    Installation, quick start, and your first application

    [:octicons-arrow-right-24: Get Started](getting-started/installation.md)

-   **Core Concepts**

    ---

    Deep dive into framework architecture and design patterns

    *Coming soon - Core concepts documentation*

-   **API Reference**

    ---

    Complete reference for all classes and methods

    *Coming soon - API reference documentation*

-   **Examples**

    ---

    Real-world applications and use cases

    *Coming soon - Example applications*

</div>

## 🤝 Contributing

This is an educational project! Contributions are welcome:

- 🐛 **Bug Reports** - Help improve the framework
- 📚 **Documentation** - Make learning easier for others
- 💡 **Examples** - Share your educational use cases
- 🎓 **Learning Content** - Add tutorials and explanations

[View Repository](https://github.com/itx-nasir/nasirpy){ .md-button }

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/itx-nasir/nasirpy/blob/master/LICENSE) file for details.

---

<div align="center">

**Built with 💡 for learning and understanding**

[⭐ Star on GitHub](https://github.com/itx-nasir/nasirpy){ .md-button }

</div> 