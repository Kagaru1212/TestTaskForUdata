from sqlalchemy import Column, Integer, String, Numeric, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import relationship

from src.auction.enums import LotStatus
from src.database import Base

class Lot(Base):
    __tablename__ = "lots"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    start_price = Column(Numeric, nullable=False)
    current_price = Column(Numeric, nullable=False)
    status = Column(Enum(LotStatus), default=LotStatus.running, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    ends_at = Column(DateTime(timezone=True), nullable=True)

    bids = relationship("Bid", back_populates="lot", cascade="all, delete-orphan")


class Bid(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True, index=True)
    lot_id = Column(Integer, ForeignKey("lots.id", ondelete="CASCADE"), nullable=False)
    bidder = Column(String, nullable=False)
    amount = Column(Numeric, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    lot = relationship("Lot", back_populates="bids")