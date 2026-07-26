from __future__ import annotations

import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.routers.weather import router as weather_router

router = APIRouter(prefix="/decideflight", tags=["decideflight"])

router.include_router(weather_router)

_STATIC_INDEX = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "static",
    "decideflight",
    "index.html",
)


@router.get("/", include_in_schema=False)
def decideflight_index() -> FileResponse:
    if not os.path.isfile(_STATIC_INDEX):
        raise HTTPException(status_code=404, detail="DecideFlight page not found")
    return FileResponse(_STATIC_INDEX, media_type="text/html; charset=utf-8")
