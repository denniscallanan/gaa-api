import uvicorn

from fastapi import FastAPI

from src.api.base import db
from src.api.team import TeamClient
from src.api.player import PlayerClient
from src.api.referee import RefereeClient
from src.api.venue import VenueClient
from src.api.match import MatchClient
from src.api.championship import ChampionshipClient

from src.constants import ServerConfig
from src.logger import logger


app = FastAPI()

version = 1

GATEWAY_PATH = f"/api/v{version}"

team_client = TeamClient()
player_client = PlayerClient()
referee_client = RefereeClient()
venue_client = VenueClient()
match_client = MatchClient()
championship_client = ChampionshipClient()


@app.middleware("http")
async def log_requests(request, call_next):
    db.connect(reuse_if_open=True)
    path = request.url.path
    response = await call_next(request)
    logger.info(f"Path: {path}; Status Code: {response.status_code}")
    if not db.is_closed():
        db.close()
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


@app.get(GATEWAY_PATH + '/players/{player_id}')
def get_player(player_id):
    return player_client.get_player(player_id)


@app.get(GATEWAY_PATH + '/referees/{referee_id}')
def get_referee(referee_id):
    return referee_client.get_referee(referee_id)


@app.get(GATEWAY_PATH + '/venues/{venue_id}')
def get_venue(venue_id):
    return venue_client.get_venue(venue_id)


@app.get(GATEWAY_PATH + '/matches/{match_id}')
def get_match(match_id):
    return match_client.get_match(match_id)


@app.get(GATEWAY_PATH + '/championships/{championship_id}')
def get_championship(championship_id):
    return championship_client.get_championship(championship_id)


if __name__ == "__main__":
    logger.info(f"Starting app on port {ServerConfig.PORT}")
    uvicorn.run("run_server:app", host='0.0.0.0',
                port=ServerConfig.PORT,
                access_log=False)
