from typing import List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from container import Container
from core.dependencies import get_current_user
from core.schema.base_schema import Blank
from core.schema.character_schema import UpdateCharacter
from core.schema.user_schema import User
from core.security import JWTBearer
from core.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(JWTBearer())]
)


@router.get("", response_model=List[User], dependencies=[Depends(get_current_user)])
@inject
async def get_users(
        service: UserService = Depends(Provide[Container.user_service])
):
    users = service.get_list()
    return users


@router.get("/{id}", response_model=User, dependencies=[Depends(get_current_user)])
@inject
async def get_user(
        id: int,
        service: UserService = Depends(Provide[Container.user_service]),
):
    return service.get_by_id(id)


@router.patch("/{id}", response_model=User, dependencies=[Depends(get_current_user)])
@inject
async def update_user(
        id: int,
        user: UpdateCharacter,
        service: UserService = Depends(Provide[Container.user_service])
):
    return service.patch(id, user)


@router.delete("/{id}", response_model=Blank, dependencies=[Depends(get_current_user)])
@inject
async def delete_user(
        id: int,
        service: UserService = Depends(Provide[Container.user_service])
):
    return service.remove_by_id(id)
