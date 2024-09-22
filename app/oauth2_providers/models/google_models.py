from pydantic import BaseModel, EmailStr


class GoogleUser(BaseModel):
    id: str
    email: EmailStr
    verified_email: bool
    name: str
    given_name: str
    family_name: str
    picture: str
