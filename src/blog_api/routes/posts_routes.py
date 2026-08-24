from fastapi import APIRouter, status
from blog_api.controllers import posts_controllers
from blog_api.models.posts_model import CreatePost

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_posts():
    return await posts_controllers.get_all_posts()


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_post_by_id(id: str):
    return await posts_controllers.get_by_id(int(id))


@router.post("/new_post", status_code=status.HTTP_201_CREATED)
async def create_post(post: CreatePost):
    return await posts_controllers.create(post)
