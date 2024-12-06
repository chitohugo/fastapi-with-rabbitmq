from typing import List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, BackgroundTasks

from container import Container
from core.dependencies import get_current_user
from core.models.user import User
from core.schema.base_schema import Blank
from core.schema.character_schema import PostCharacter, UpdateCharacter, Character
from core.security import JWTBearer
from core.services.character_service import CharacterService
from core.services.rabbitmq_service import RabbitMQService

router = APIRouter(
    prefix="/characters",
    tags=["characters"],
    dependencies=[Depends(JWTBearer())]
)


@router.get("", response_model=List[Character], dependencies=[Depends(get_current_user)])
@inject
async def get_characters(
        service: CharacterService = Depends(Provide[Container.character_service])
):
    characters = service.get_list()
    return characters


@router.get("/{id}", response_model=Character, dependencies=[Depends(get_current_user)])
@inject
async def get_character(
        id: int,
        service: CharacterService = Depends(Provide[Container.character_service])
):
    return service.get_by_field("id", id)


@router.post("", response_model=Character)
@inject
async def create_character(
        payload: PostCharacter,
        background_tasks: BackgroundTasks,
        service: CharacterService = Depends(Provide[Container.character_service]),
        rabbitmq: RabbitMQService = Depends(Provide[Container.rabbitmq_service]),
        current_user: User = Depends(get_current_user)
):
    payload.user_id = current_user.id
    character = service.add(payload)
    background_tasks.add_task(
        rabbitmq.publish,
        routing_key="character_created",
        message=payload.model_dump()
    )
    return character


@router.patch("/{id}", response_model=Character, dependencies=[Depends(get_current_user)])
@inject
async def update_character(
        id: int,
        payload: UpdateCharacter,
        service: CharacterService = Depends(Provide[Container.character_service])
):
    return service.patch(id, payload)


@router.delete("/{id}", response_model=Blank, dependencies=[Depends(get_current_user)])
@inject
async def delete_character(
        id: int,
        service: CharacterService = Depends(Provide[Container.character_service])
):
    return service.remove_by_id(id)
