from fastapi import APIRouter
from .routers import info, static_server, auth, upload, level, proxy, posts
from . import models

router = APIRouter(prefix='/sonolus')

router.include_router(info.router)
router.include_router(static_server.router)
router.include_router(auth.router)
router.include_router(upload.router)
router.include_router(level.router)
router.include_router(proxy.router)
router.include_router(posts.router)

__all__ = ['router', 'models']