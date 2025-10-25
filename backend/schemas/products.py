from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class ProductDB(BaseModel):
    name: str
    price: float
    created_at: Optional[datetime] = None

class ProductReadSchema(ProductDB):
    id: int
    
    class Config:
        orm_mode = True
        

class ProductCreateSchema(ProductDB):
    pass 

class ProductUpdateSchema(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
