import bcrypt
from fastapi import APIRouter, Depends, Response, HTTPException,status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi_jwt_auth.exceptions import MissingTokenError, InvalidHeaderError
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_async_db
from models.users import Users
from schemas.users.login import UserLogin

auth_router = APIRouter(prefix="/user", tags=["user"])


@auth_router.post("/login")
async def login_user(user_data:UserLogin, Authorize: AuthJWT=Depends(), db: AsyncSession=Depends(get_async_db)):

    try:
        Authorize.jwt_required()
        return RedirectResponse(url="/product/product_list")
    
    # except Exception as error:
    #     return Response({"message": str(error)}, status_code=status.HTTP_400_BAD_REQUEST)
    
    except (MissingTokenError, InvalidHeaderError):
        user_stmt = await db.execute(select(Users).where(Users.email==user_data.email))
        user = user_stmt.scalars().first()

        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user not found")
        

        password_bytes = user_data.password.encode("utf-8")
        stored_password_bytes = user.password_hash.encode("utf-8")
        check_password = bcrypt.checkpw(password_bytes, stored_password_bytes)

        if not check_password:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="passwords are not match")

        user.is_active = True
        await db.commit()
        await db.refresh(user)

        access_token = Authorize.create_access_token(subject=user_data.email)
        refresh_token = Authorize.create_refresh_token(subject=user_data.email)

        return JSONResponse(content={"access_token": access_token, "refresh_token": refresh_token})




@auth_router.post("/register")
async def register_user(user_data: UserLogin, db: AsyncSession=Depends(get_async_db)):
    user_stmt = await db.execute(select(Users).where(Users.email==user_data.email))
    user = user_stmt.scalars().first()

    if user is not None and not user.is_active:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "user already exists"})
    

    hashed_password = bcrypt.hashpw(user_data.password.encode("utf-8"), bcrypt.gensalt())
    hashed_password_str = hashed_password.decode("utf-8")  


    new_user = Users(email=user_data.email, password_hash=hashed_password_str)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "new_user was created"})
