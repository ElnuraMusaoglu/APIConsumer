from fastapi import APIRouter

from app.api.routes import groups, cluster

router = APIRouter()
router.include_router(groups.router, tags=["groups"], prefix="/groups")
router.include_router(cluster.router, tags=["cluster"], prefix="/cluster")
