from functools import wraps
from fastapi import Depends, HTTPException, status
from fastapi_jwt_auth.exceptions import MissingTokenError, InvalidHeaderError
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_async_db
from models.users import Users
from models.products import Product


def is_authenticated(Autorize: AuthJWT=Depends()):
    try:
        Autorize.jwt_required()
    
    except (MissingTokenError, InvalidHeaderError):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user got to be logged in")

    return Autorize
        


def is_owner(product,  user, db: AsyncSession=Depends(get_async_db)) -> bool:
    # product_stmt = await db.execute(select(Product).where(Product.id==product_id))
    # product = product_stmt.scalars().first()

    # if product is None:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="product is not found")
        
    return product.user_id != user.id



def is_product_owner(func):
    @wraps(func)
    async def wrapper(product_id: int, db: AsyncSession=Depends(get_async_db), Authorize: AuthJWT=Depends(), *args, **kwargs):
        current_user = Authorize.get_jwt_subject()
        user_stmt = await db.execute(select(Users).where(Users.email==current_user))
        user = user_stmt.scalars().first()

        product_stmt = await db.execute(select(Product).where(Product.id==product_id))
        product = product_stmt.scalars().first()

        if product.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        
        return await func(product_id=product_id, db=db, Authorize=Authorize, *args, **kwargs)

    return wrapper
        