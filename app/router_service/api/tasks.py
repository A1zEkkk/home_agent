import asyncio
import logging
import time
import uuid

from fastapi import APIRouter, Depends, Request
from .model.request import *


router = APIRouter()

lock = asyncio.Lock()

logger = logging.getLogger("router_service")

def get_client():
    from app.router_service.main import client
    return client

@router.post("/process")
async def process(request: TextRequest, client = Depends(get_client)):
    #if lock.locked():# Оверсток. У нас очень быстро все работает 1-2 токена делает. В роутере излешне
    #    return await send_to_queue(QueueRequest(text=request.text)) #В будущем доделать сейчас заглушка, которая должна будет брокеру задачу на обработку отправлять

    try:
        await lock.acquire()
        service = await asyncio.to_thread(client.route, request.text)
        return {"status": "done", "service": service}
    finally:
        lock.release()


@router.post("/queue")
async def send_to_queue(request: QueueRequest):
    return {
        "status": "queued",
        "message": f"Task '{request.text}' sent to broker"
    }

async def logging_middleware(request: Request, call_next):
    request_id = uuid.uuid4().hex[:8]
    start_time = time.time()

    body = await request.body()

    logger.info(
        f"[{request_id}] Incoming request | path={request.url.path} | size={len(body)}"
    )

    response = await call_next(request)

    duration = round((time.time() - start_time) * 1000, 2)

    logger.info(
        f"[{request_id}] Request completed | time={duration}ms"
    )

    return response