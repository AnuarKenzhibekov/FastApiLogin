from fastapi import FastAPI, Depends,Response
from authx import AuthX, AuthXConfig
from pydantic import BaseModel
from fastapi import HTTPException


app = FastAPI()

config = AuthXConfig(
    JWT_SECRET_KEY="SECRET_KEY",
    JWT_ACCESS_COOKIE_NAME="my_access_token",
    JWT_TOKEN_LOCATION=["cookies"]
)

security = AuthX(config=config)

class UserLoginSchema(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(credentials: UserLoginSchema, response: Response):
    if credentials.username == "admin" and credentials.password == "admin":
        token = security.create_access_token(uid="12345")
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Incorrect username or password")

@app.get("/protected", dependencies=[Depends(security.access_token_required)])
def protected():
    return {"data": "TOP SECRET"}