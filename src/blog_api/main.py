from fastapi import FastAPI
from blog_api.routes import posts_routes

app = FastAPI()

app.include_router(posts_routes.router, tags=["Posts"])
