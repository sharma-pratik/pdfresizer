from pydantic import BaseModel, EmailStr, constr


class SignupSchema(BaseModel):

    full_name: constr(max_length=40)
    email: EmailStr
    password : constr(max_length=40)

class LoginSchema(BaseModel):

    email: EmailStr
    password : constr(max_length=40)