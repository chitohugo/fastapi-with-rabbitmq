from core.schema.user_schema import User
from core.services.auth_service import AuthService
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from container import Container
from core.schema.auth_schema import SignIn, SignInResponse, SignUp

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/sign-in", response_model=SignInResponse)
@inject
async def sign_in(payload: SignIn, service: AuthService = Depends(Provide[Container.auth_service])):
    return service.sign_in(payload)


@router.post("/sign-up", response_model=User)
@inject
async def sign_up(payload: SignUp, service: AuthService = Depends(Provide[Container.auth_service])):
    return service.sign_up(payload)
