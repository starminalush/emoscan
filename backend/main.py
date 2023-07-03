from api.api import router
from core.db.database import Base, engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app():
    new_app = FastAPI()
    new_app.include_router(router)
    return new_app


app = create_app()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown_event():
    await engine.dispose()
