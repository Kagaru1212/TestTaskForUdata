import asyncio

from fastapi import FastAPI

from src.auction.tasks import auction_watcher
from src.auction.routers import router as auction_router
from src.auction.ws.routers import router as web_socket_router

app = FastAPI()
app.include_router(auction_router)
app.include_router(web_socket_router)

@app.on_event("startup")
async def start_background_tasks():
    asyncio.create_task(auction_watcher())