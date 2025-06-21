from pydantic import BaseModel


class BaseScheme(BaseModel):
    class Config:
        from_attributes = True
