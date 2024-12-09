import time

from fastapi import Request
import logging

logger = logging.getLogger(__name__)


async def log_requests(request: Request, call_next):
    logger.info(f"URL: {request.url}")
    logger.info(f"Method: {request.method}")
    logger.info(f"Headers: {dict(request.headers)}")

    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    logger.info(f"Response received (time: {process_time:.4f} seconds)")

    return response
