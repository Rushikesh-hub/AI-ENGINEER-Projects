from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email:EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class DocumentOut(BaseModel):
    id:int
    filename:str
    parsed_text:str | None

    class Config:
        form_attributes = True