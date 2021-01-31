import traceback
import uvicorn
import threading

from fastapi import FastAPI, HTTPException

from src.api.client import Client
from src.api.models import RawParticipantData
from src.constants import ServerConfig, ErrorValues
from src.logger import logger


app = FastAPI()

version = 1

GATEWAY_PATH = f"/api/v{version}"


@app.middleware("http")
async def log_requests(request, call_next):
    path = request.url.path
    response = await call_next(request)
    logger.info(f"Path: {path}; Status Code: {response.status_code}")
    return response


@app.get('/')
def root():
    return {"result": f"Use {GATEWAY_PATH}/healthcheck to check the health of the server"}


@app.get(GATEWAY_PATH + '/healthcheck')
def healthcheck():
    return {"status": "ok"}


if __name__ == "__main__":
    logger.info(f"Starting app on port {ServerConfig.PORT}")
    uvicorn.run("run_server:app", host='0.0.0.0',
                port=ServerConfig.PORT,
                access_log=False)
