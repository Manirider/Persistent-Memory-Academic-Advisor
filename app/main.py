from fastapi import FastAPI
from app.api import health, tools, memory
from app.db.database import init_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Academic Advisor API")

app.include_router(health.router)
app.include_router(tools.router)
app.include_router(memory.router)


@app.on_event("startup")
def startup_event():
    init_db()
    logger.info("Database initialized")


@app.get("/")
def root():
    return {"message": "Academic Advisor API"}
