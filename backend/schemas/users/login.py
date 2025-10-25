from pydantic import BaseModel
from typing import Optional

class UserLogin(BaseModel):
    email: str
    password: str
    is_active: Optional[bool] = None