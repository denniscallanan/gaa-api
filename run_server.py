import uvicorn
import psycopg2

from fastapi import FastAPI

from src.api.team import TeamClient
from src.constants import ServerConfig
from src.logger import logger


app = FastAPI()

version = 1

GATEWAY_PATH = f"/api/v{version}"

conn = psycopg2.connect(ServerConfig.DATABASE_URL)

team_client = TeamClient(conn)

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


@app.get(GATEWAY_PATH + '/teams/{team_id}')
def get_team(team_id):
    return team_client.get_team(team_id)

if __name__ == "__main__":
    logger.info(f"Starting app on port {ServerConfig.PORT}")
    uvicorn.run("run_server:app", host='0.0.0.0',
                port=ServerConfig.PORT,
                access_log=False)
