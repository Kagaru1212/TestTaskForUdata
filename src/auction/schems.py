from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class BidBase(BaseModel):
    bidder: str
    amount: float


class BidCreate(BidBase):
    pass


class BidRead(BidBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class LotBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_price: float = Field(..., gt=5)


class LotCreate(LotBase):
    ends_at: Optional[datetime] = None


class LotRead(LotBase):
    id: int
    current_price: float
    status: str
    created_at: datetime
    ends_at: Optional[datetime]

    class Config:
        from_attributes = True
