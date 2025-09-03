import asyncio
from datetime import datetime
from sqlalchemy.orm import Session
from src.database import SessionLocal
from .models import Lot

async def auction_watcher():
    """
    Background task that periodically checks for lots whose auction has ended.

    This coroutine runs indefinitely, sleeping for 10 seconds between checks.
    For each lot whose end time has passed and is still running, it updates
    the status to 'ended' in the database.
    """
    while True:
        await asyncio.sleep(10)
        db: Session = SessionLocal()
        try:
            lots = db.query(Lot).filter(Lot.status=="running", Lot.ends_at <= datetime.utcnow()).all()
            for lot in lots:
                lot.status = "ended"
            db.commit()
        finally:
            db.close()
