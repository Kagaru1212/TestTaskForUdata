from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from src.auction.models import Lot
from src.database import get_db

router = APIRouter()

active_connections: dict[int, set[WebSocket]] = {}


@router.websocket("/ws/lots/{lot_id}/")
async def lot_ws(websocket: WebSocket, lot_id: int,  db: Session = Depends(get_db)):
    await websocket.accept()

    # Validate that the lot exists and is active
    lot = db.query(Lot).filter(Lot.id == lot_id).first()
    if not lot:
        await websocket.send_json({"error": "Lot not found"})
        await websocket.close(code=1008)  # Policy Violation
        return

    if lot.status != "running":
        await websocket.send_json({"error": "Lot is not active"})
        await websocket.close(code=1008)  # Policy Violation
        return

    if lot_id not in active_connections:
        active_connections[lot_id] = set()
    active_connections[lot_id].add(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass

    finally:
        active_connections[lot_id].discard(websocket)
        if not active_connections[lot_id]:
            del active_connections[lot_id]
