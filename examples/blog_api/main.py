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

@app.get("/users/{user_id}")
async def get_user(request):
    user_id = request.path_params["user_id"]
    return Response({
        "message": f"Getting user {user_id}",
        "user_id": user_id
    })

@app.get("/users/{user_id}/posts/{post_id}")
async def get_user_post(request):
    user_id = request.path_params["user_id"]
    post_id = request.path_params["post_id"]
    return Response({
        "message": f"Getting post {post_id} for user {user_id}",
        "user_id": user_id,
        "post_id": post_id
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
