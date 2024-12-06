from fastapi import APIRouter
from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.characters import router as character_router
from app.api.endpoints.users import router as user_router

routers = APIRouter()
router_list = [auth_router, user_router, character_router]

[routers.include_router(router) for router in router_list]
