from nasirpy import App, Response

app = App()

@app.get("/")
async def hello(request):
    return Response({"message": "Hello, World!"})

@app.post("/items")
async def create_item(request):
    body = await request.body()
    # Handle item creation
    return Response({"status": "created"}, status_code=201)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
