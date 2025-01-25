from pydantic import BaseModel, EmailStr

class BaseUser(BaseModel):
    pass

class UserRegisterSchema(BaseUser):
    email: EmailStr
    password: str

class UserLoginSchema(UserRegisterSchema):
    pass
