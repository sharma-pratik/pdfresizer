from os import stat
from auth.models import AppUser
from auth.schema import SignupSchema, LoginSchema
from fastapi import APIRouter
from db_config import DB
from fastapi import FastAPI, Response, status
from auth.utils import get_hashed_pwd, validate_pwd, JWTManager
from fastapi.responses import JSONResponse

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@auth_router.post("/signup")
def signup(user_info : SignupSchema):

    user_info = user_info.dict()
    user_email = user_info.get("email")
    existing_user = DB.query(AppUser).filter(AppUser.email == user_info.get("email")).count()
    
    if existing_user:
        response_data =  {
            "success" :  False,
            "data" : {"email" : f"User with the given {user_email} email already exists."},
        }

        return JSONResponse(
            content=response_data, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, media_type="application/json",
        )
    else:
        hash_pwd = get_hashed_pwd(user_info.get("password"))
        user_info["password"] = hash_pwd
        user = AppUser(**user_info)
        DB.add(user)
        DB.commit()

    return JSONResponse(
        content={
            "success" :  True,
            "msg" : "User created successfully."
        },
        media_type="application/json",
        status_code= status.HTTP_201_CREATED
    )


@auth_router.post("/login")
def login(user_info : LoginSchema):
    
    user_info = user_info.dict()
    user_email = user_info.get("email")
    pwd = user_info.get("password")
    
    existing_user = DB.query(AppUser).filter(AppUser.email == user_info.get("email")).first()
    
    response_status_code = None
    response_data = {}
    
    if existing_user:
        if validate_pwd(pwd, existing_user.password):
            encoded_data = {
                "email" : user_email
            }

            jwt_manager = JWTManager()
            token = jwt_manager.get_jwt_token(payload=encoded_data)

            response_data = {
                "success" : True,
                "data" : {
                    "token" : token
                }
            }
            response_status_code = status.HTTP_200_OK

        else:
            response_data =  {
                "success" :  False,
                "data" : {"password" : "Incorrect password"},
            }
            response_status_code = status.HTTP_401_UNAUTHORIZED

    else:
        response_data =  {
            "success" :  False,
            "data" : {"email" : f"User with the given {user_email} email does not exists."},
        }
        response_status_code = status.HTTP_404_NOT_FOUND

    return JSONResponse(
        content=response_data,
        media_type="application/json",
        status_code= response_status_code
    )
