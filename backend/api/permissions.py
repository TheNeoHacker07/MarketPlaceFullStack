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
        


async def is_owner(product,  user, db: AsyncSession=Depends(get_async_db)) -> bool:
    # product_stmt = await db.execute(select(Product).where(Product.id==product_id))
    # product = product_stmt.scalars().first()

    # if product is None:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="product is not found")


    if product.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="not your product")
    return True


