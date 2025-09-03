from pydantic import BaseModel, Field, validator
from datetime import datetime, timedelta, timezone
from typing import Optional


class BidBase(BaseModel):
    bidder: str = Field(..., min_length=2, max_length=50, description="Bidder's name, 2-50 characters")
    amount: float = Field(..., gt=0, description="Bid amount must be positive")


class BidCreate(BidBase):
    pass


class BidRead(BidBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class LotBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="Lot title, 3-100 chars")
    description: Optional[str] = Field(None, max_length=500, description="Optional description, up to 500 chars")
    start_price: float = Field(..., gt=5, description="Start price must be greater than 5")


class LotCreate(LotBase):
    ends_at: datetime

    @validator("ends_at", pre=True, always=True)
    def validate_ends_at(cls, v):
        now = datetime.now(timezone.utc)
        if isinstance(v, str):
            try:
                v = datetime.fromisoformat(v)
            except ValueError:
                raise ValueError("ends_at must be a valid ISO datetime")
        if v <= now:
            raise ValueError("ends_at cannot be in the past")
        if v > now + timedelta(hours=1):
            raise ValueError("ends_at cannot be more than 1 hour from now")
        if v < now + timedelta(minutes=5):
            raise ValueError("ends_at must be at least 5 minutes from now")
        return v


class LotRead(LotBase):
    id: int
    current_price: float
    status: str
    created_at: datetime
    ends_at: Optional[datetime]

    class Config:
        from_attributes = True
