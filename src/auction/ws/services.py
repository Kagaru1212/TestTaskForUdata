from src.auction.ws.routers import active_connections


async def notify_bid(lot_id: int, bidder: str, amount: float):
    if lot_id in active_connections:
        for ws in active_connections[lot_id]:
            await ws.send_json({
                "type": "bid_placed",
                "lot_id": lot_id,
                "bidder": bidder,
                "amount": float(amount)
            })
