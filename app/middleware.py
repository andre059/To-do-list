from fastapi import Request
import logging

logger = logging.getLogger(__name__)


async def log_requests(request: Request):
    logger.info(f"URL: {request.url}")
    logger.info(f"Method: {request.method}")
    logger.info(f"Headers: {dict(request.headers)}")
