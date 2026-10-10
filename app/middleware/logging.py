import logging

from fastapi import Request


logger = logging.getLogger(__name__)


async def log_requests(request: Request, call_next):
    response = await call_next(request)

    logger.info(
        "%s %s → %s",
        request.method,
        request.url.path,
        response.status_code,
    )

    return response