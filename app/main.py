from fastapi import FastAPI, Request
from app.routes.dashboard import router as dashboard_router
from app.models.models import init_db

app = FastAPI()
init_db()

app.include_router(dashboard_router)
