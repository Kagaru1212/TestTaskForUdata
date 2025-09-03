from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from src.auction.models import Lot, Bid
from src.auction.schemas import LotCreate, BidCreate


def create_lot(db: Session, lot_data: LotCreate) -> Lot:
    """
    Create a new lot in the database.

    Args:
        db (Session): SQLAlchemy database session.
        lot_data (LotCreate): Pydantic model with lot creation data.

    Returns:
        Lot: The newly created Lot object.
    """
    lot = Lot(
        title=lot_data.title,
        description=lot_data.description,
        start_price=lot_data.start_price,
        current_price=lot_data.start_price,
        created_at=datetime.utcnow(),
        ends_at=lot_data.ends_at,
    )
    db.add(lot)
    db.commit()
    db.refresh(lot)
    return lot

def list_lots(db: Session):
    """
    List all running lots.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        list[Lot]: A list of all lots that are currently running.
    """
    return db.query(Lot).filter(Lot.status == "running").all()

def place_bid(db: Session, lot_id: int, bid_data: BidCreate) -> Bid:
    """
    Place a new bid on a lot.

    Args:
        db (Session): SQLAlchemy database session.
        lot_id (int): ID of the lot to bid on.
        bid_data (BidCreate): Pydantic model with bid details.

    Returns:
        Bid: The newly created Bid object.

    Raises:
        ValueError: If the lot does not exist, is not running, or bid is too low.
    """
    lot = db.query(Lot).filter(Lot.id == lot_id).first()
    if not lot:
        raise ValueError("Lot not found")
    if lot.status != "running":
        raise ValueError("Lot is not running")
    if bid_data.amount <= lot.current_price:
        raise ValueError("Bid must be higher than current price")

    bid = Bid(
        lot_id=lot.id,
        bidder=bid_data.bidder,
        amount=bid_data.amount,
        created_at=datetime.utcnow()
    )
    db.add(bid)

    # Update lot's current price and extend end time by 30 seconds
    lot.current_price = bid_data.amount
    lot.ends_at += timedelta(seconds=30)

    db.commit()
    db.refresh(bid)
    db.refresh(lot)
    return bid