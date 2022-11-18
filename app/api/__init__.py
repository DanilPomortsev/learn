from fastapi import APIRouter
from app.api.user import user_router, post_router, sub_router, photo_router, auth_router

router = APIRouter()
router.include_router(user_router)
router.include_router(post_router)
router.include_router(sub_router)
router.include_router(photo_router)
router.include_router(auth_router)