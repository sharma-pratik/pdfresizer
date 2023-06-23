import hashlib
import jwt
from config import SECRET_KEY
import datetime
from datetime import timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from fastapi import Request, HTTPException


def get_hashed_pwd(raw_pwd):
    hash_pwd = hashlib.sha512(raw_pwd.encode()).hexdigest()
    return hash_pwd

def validate_pwd(raw_pwd, salted_pwd):

    hash_pwd = get_hashed_pwd(raw_pwd)

    return hash_pwd == salted_pwd


class JWTManager:

    EXPIRY_TIME_IN_HOUR = 4
    SECRET_KEY = SECRET_KEY
    ALGO = "HS256"

    def __init__(self) -> None:
        self.error = None

    def get_jwt_token(self, payload):   

        payload.update(
            {
                "exp" : datetime.datetime.utcnow() + timedelta(hours=self.EXPIRY_TIME_IN_HOUR)
            }
        )
        encoded_jwt = jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGO)
        return encoded_jwt

    def decode_jwt(self, token):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=self.ALGO)
            return payload
        except jwt.ExpiredSignatureError:
            self.error = "Token is expired"
        except jwt.InvalidSignatureError:
            self.error = "Invalid token"
        except jwt.InvalidTokenError:
            self.error = "Invalid token"
        except Exception as e:
            self.error = "Can not processed this token"

# class JWTBearer(HTTPBearer):
#     def __init__(self, auto_error: bool = True):
#         super(JWTBearer, self).__init__(auto_error=auto_error)

#     async def __call__(self, request: Request):
#         credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
#         if credentials:
#             if not credentials.scheme == "Bearer":
#                 raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            
#             jwtmanager = JWTManager()

#             payload = jwtmanager.decode_jwt(credentials.credentials)

#             if jwtmanager.error:
#                 raise HTTPException(status_code=403, detail="Invalid token or expired token.")
#             else:
#                 return credentials.credentials
#         else:
#             raise HTTPException(status_code=403, detail="Invalid authorization code.")

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = JWTManager().decode_jwt(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid