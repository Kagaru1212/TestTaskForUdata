from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.auction.ws.services import notify_bid
from src.auction.schemas import LotCreate, LotRead, BidRead, BidCreate
from src.auction.services import create_lot, list_lots, place_bid
from src.database import get_db

router = APIRouter(
    tags=["Auction"],
)


@router.get("/lots", response_model=List[LotRead])
def get_lots(db: Session = Depends(get_db)):
    """
    Get all active lots.
    """
    lots = list_lots(db)
    return lots

@router.post("/lots", response_model=LotRead)
def create_lot_endpoint(lot: LotCreate, db: Session = Depends(get_db)):
    """
    Create a new lot.
    - `title` — lot title
    - `description` — lot description
    - `start_price` — starting price
    - `ends_at` — auction end time (must be between +5 minutes and +1 hour from now)
    """
    db_lot = create_lot(db, lot)
    return db_lot


@router.post("/lots/{lot_id}/bids", response_model=BidRead)
async def create_bid(lot_id: int, bid: BidCreate, db: Session = Depends(get_db)):
    """
    Place a bid on a lot.
    - `lot_id` — ID of the lot
    - `bidder` — bidder name
    - `amount` — bid amount (must be greater than the current price)

    On success:
    - lot price is updated
    - auction time is extended by +30 seconds
    - all WebSocket subscribers are notified with `bid_placed` event
    """
    try:
        db_bid = place_bid(db, lot_id, bid)
        # Notify all WebSocket clients about the new bid
        await notify_bid(db_bid.lot_id, db_bid.bidder, db_bid.amount)
        return db_bid

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

