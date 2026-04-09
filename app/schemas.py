from pydantic import BaseModel

class Config:
    from_attributes = True

class GuestCreate(BaseModel):
    name: str
    relation: str

class GuestUpdate(BaseModel):
    amount: int

class GuestResponse(BaseModel):
    id: int
    name: str
    relation: str
    shagun_amount: int
    status: str

    class Config:
        orm_mode = True
