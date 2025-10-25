from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError, InvalidHeaderError, JWTDecodeError
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.products import Product, Cart, CartItem, Order
from models.users import Users
from .permissions import is_authenticated, is_product_owner
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


@product_router.post("/add_product/")
async def add_product(product_create_data: ProductCreateSchema, Authorize: AuthJWT=Depends(is_authenticated), db: AsyncSession=Depends(get_async_db)):


    current_user_email = Authorize.get_jwt_subject()
    user_stmt = await db.execute(select(Users).where(Users.email==current_user_email))
    user = user_stmt.scalars().first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="uou got to be logged in")


    new_product = Product(**product_create_data.dict(),user_id=user.id)
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)


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


@is_product_owner
@product_router.delete("/product_delete/{product_id}")
async def delete_product(product_id: int, Autрorize: AuthJWT=Depends(), db: AsyncSession=Depends(get_async_db)):
    try:
        Autрorize.jwt_required()
    except (MissingTokenError, InvalidHeaderError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you gotta be logged in")

    except JWTDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="expired token")

    product = await get_special_product(product_id, db)
        
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    current_user_email = Autрorize.get_jwt_subject()
    user_stmt = await db.execute(select(Users).where(Users.email==current_user_email))
    user = user_stmt.scalars().first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="uou got to be logged in")


  
    await db.delete(product)
    await db.commit()
    
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "product was deleted"})





@product_router.post("/add_to_item/{product_id}")
async def add_to_item(product_id: int, Authorize: AuthJWT=Depends(), db: AsyncSession=Depends(get_async_db)):
    product = await get_special_product(product_id, db)

    if product is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="product not found")
    
    try:
        Authorize.jwt_required()
    except (MissingTokenError, InvalidHeaderError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you gotta be logged in")
    except JWTDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="expired token")


    current_user = Authorize.get_jwt_subject()


    cart_stmt = await db.execute(select(Cart).where(Cart.user.has(email=current_user)))
    cart = cart_stmt.scalars().first()


    cart_item_stmt = await db.execute(select(CartItem).where(CartItem.cart_id==cart.id).where(CartItem.product_id==product_id))
    cart_item = cart_item_stmt.scalars().first()

    if cart_item:
        cart_item.quantity += 1
        db.add(cart_item)
        await db.commit()
        await db.refresh(cart_item)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "updated quantity"})

    new_cart_item = CartItem(cart_id=cart.id, product_id=product.id)
    db.add(new_cart_item)
    await db.commit()
    await db.refresh(new_cart_item)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "new_cart was created"})


@is_product_owner
@product_router.delete("/remove_cart_item/{product_id}")
async def remove_cart_item(product_id: int, Authorize:AuthJWT=Depends(), db: AsyncSession=Depends(get_async_db)):
    
    try:
        Authorize.jwt_required()
    except (MissingTokenError, InvalidHeaderError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you gotta be logged in")
    except JWTDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="expired token")


    product = await get_special_product(product_id, db)

    if product is None:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    
    current_user = Authorize.get_jwt_subject()
    
    cart_stmt = await db.execute(select(Cart).where(Cart.user.has(email=current_user)))
    cart = cart_stmt.scalars().first()

    cart_item_stmt = await db.execute(select(CartItem).where(CartItem.cart_id==cart.id).where(CartItem.product_id==product_id))
    cart_item = cart_item_stmt.scalars().first()

    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            db.add(cart_item)
            await db.commit()
            await db.refresh(cart_item)
            return Response(status_code=status.HTTP_200_OK)
        
        elif cart_item.quantity == 1:
            await db.delete(cart_item)
            await db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)



@product_router.post("/order_product/{cart_item_id}")
async def order_product(cart_item_id: int, Authorize: AuthJWT=Depends(), db: AsyncSession=Depends(get_async_db)):
    cart_item_stmt = await db.execute(select(CartItem).where(CartItem.id==cart_item_id))
    cart_item = cart_item_stmt.scalars().first()

    if not cart_item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
    
    current_user = Authorize.get_jwt_subject()
    user_stmt = await db.execute(select(Users).where(Users.email==current_user))
    user = user_stmt.scalars().first()

    new_order = Order(user_id=user.id, cart_item_id=cart_item_id)
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return Response(status_code=status.HTTP_201_CREATED)






