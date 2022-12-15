from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from starlette.middleware.cors import CORSMiddleware
from app.core.logging import init_logging
from app.api.routes.api import router as api_router
from app.db.db import metadata, engine, database
from app.services import rollback_service

def get_application() -> FastAPI:
    application = FastAPI()

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(api_router, prefix="/api/v1")

    return application

metadata.create_all(engine)
app = get_application()
init_logging()

@app.on_event('startup')
@repeat_every(seconds=30, wait_first=True) # 30 seconds repeated task
async def startup():
    if not database.is_connected:
        await database.connect()
    await rollback_service.check_and_send_delete_group_task()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()
    

