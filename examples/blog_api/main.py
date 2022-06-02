from nasirpy import App

app = App()

@app.get("/")
async def hello(request):
    return Response({"message": "Hello, World!"})

@app.post("/items")
async def create_item(request):
    body = await request.body()
    # Handle item creation
    return Response({"status": "created"}, status_code=201)
