import time

from fastapi import APIRouter

router = APIRouter()

_START_TIME = time.time()


@router.get("")
def health_check() -> dict[str, object]:
    """
    Service health check.

    Returns service status, version, and uptime. No auth required.
    """
    uptime_seconds = round(time.time() - _START_TIME, 2)
    return {
        "status": "ok",
        "service": "HireMindAI API",
        "version": "0.1.0",
        "uptime_seconds": uptime_seconds,
    }
