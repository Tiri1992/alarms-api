"""Main script."""
import time
from fastapi import FastAPI
from fastapi import Request
# Api routers
from app.api.api_v1 import api as apiv1
from app.core.config import settings
# Securities


# Base.metadata.create_all(engine)

app = FastAPI(
    title="Alarms API",
)

# Create a middleware timer
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Version 1, this will scale on version 2.
app.include_router(apiv1.router, prefix=settings.API_V1)