from jose import jwt, JWTError
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer

class CustomHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials = await super().__call__(request)
        if credentials:
            return credentials
        raise HTTPException(status_code=401, detail="Tum Kaun Ho?")
    
SECRET = "shagun_secret"
security = CustomHTTPBearer()

def create_token():
    return jwt.encode({"user": "admin"}, SECRET, algorithm="HS256")

def verify_token(token=Depends(security)):
    try:
        jwt.decode(token.credentials, SECRET, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Tum Kaun Ho?")
    