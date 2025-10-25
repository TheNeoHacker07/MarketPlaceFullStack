from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError, InvalidHeaderError
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.products import Product 
from models.users import Users
from permissions import is_authenticated, is_owner
from db import get_async_db
from schemas.products import ProductCreateSchema, ProductReadSchema, ProductUpdateSchema



product_router = APIRouter(prefix="/products", tags=["products"])


async def get_special_product(product_id: int, db: AsyncSession=Depends(get_async_db)):
    product_stmt = await db.execute(select(Product).where(Product.id==product_id))
    return product_stmt.scalars().one_or_none()



@product_router.get("/product_list")
async def get_product_list(db: AsyncSession=Depends(get_async_db)):
    products_stmt = await db.execute(select(Product))
    product_list = products_stmt.scalars()
    product_list_response = [
        {
            "id": product.id,
            "name": product.name,
            "created_at": str(product.created_at) 
        }
        for product in product_list
    ]
    return JSONResponse(status_code=status.HTTP_200_OK, 
                        content={"message": "get_product_list", "products": product_list_response})


@product_router.post("/add_product")
async def add_product(product_create_data: ProductCreateSchema, Authorize: AuthJWT=Depends(is_authenticated), db: AsyncSession=Depends(get_async_db)):
    new_product = Product(**product_create_data.dict())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)


    current_user_email = AuthJWT.get_jwt_subject()
    user_stmt = await db.execute(select(Users).where(Users.email==current_user_email))
    user = user_stmt.scalars().first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="uou got to be logged in")


    created_product = {"id": new_product.id, "name": new_product.name, "created_at": str(new_product.created_at)}

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"new_product": created_product})




@product_router.get("/product/{product_id}")
async def get_product(product_id: int, db: AsyncSession=Depends(get_async_db)):
    product = await get_special_product(product_id=product_id, db=db)
    
    if product is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
    product_response = {
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "created_at": str(product.created_at)
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content={"product": product_response})



@product_router.delete("/product_delete/{product_id}")
async def delete_product(product_id: int, Autorize: AuthJWT=Depends(), db: AsyncSession=Depends(get_async_db)):
    try:
        Autorize.jwt_required()
    except (MissingTokenError, InvalidHeaderError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you gotta be logged in")
    
    product = await get_special_product(product_id, db)
        
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    current_user_email = Autorize.get_jwt_subject()
    user_stmt = await db.execute(select(Users).where(Users.email==current_user_email))
    user = user_stmt.scalars().first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="uou got to be logged in")


    permission_result = await is_owner(product, user, db) 
    
    if permission_result is not True:
        return permission_result
    
    await db.delete(product)
    await db.commit()
    
    return Response(content={"message": "product was deleted"}, status_code=status.HTTP_204_NO_CONTENT)



