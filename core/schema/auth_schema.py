from pydantic import BaseModel


class SignIn(BaseModel):
    email: str
    password: str


class SignUp(SignIn):
    first_name: str
    last_name: str
    username: str


class Payload(BaseModel):
    id: int
    email: str
    first_name: str


class SignInResponse(BaseModel):
    access_token: str
