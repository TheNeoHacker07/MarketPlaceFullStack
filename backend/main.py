from pydantic import BaseModel
from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
import uvicorn
from api.products import product_router
from api.users import auth_router
from sockets.socket import socket_router

app = FastAPI()
app.include_router(product_router)
app.include_router(auth_router)

class AuthSettings(BaseModel):
    authjwt_secret_key: str = "e9a49cf42a48c2c482de15e75f4c6e28e7b8c89944d7e3fcd982dfc9938b0b8c"
    authjwt_access_token_expires: int = 3600       # срок действия access token в секундах (1 час)
    authjwt_refresh_token_expires: int = 86400


@AuthJWT.load_config
def get_confing():
    return AuthSettings()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)