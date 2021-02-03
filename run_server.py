from typing import Optional

import uvicorn

from fastapi import FastAPI, Header, HTTPException
from fastapi.openapi.utils import get_openapi

from src.api.clients.base import db
from src.api.clients.team import TeamClient, TeamResponseModel
from src.api.clients.team_manager import TeamManagerClient, TeamManagerResponseModel
from src.api.clients.player import PlayerClient, PlayerResponseModel
from src.api.clients.referee import RefereeClient, RefereeResponseModel
from src.api.clients.venue import VenueClient, VenueResponseModel
from src.api.clients.match import MatchClient, MatchResponseModel
from src.api.clients.championship import ChampionshipClient, ChampionshipResponseModel
from src.api.clients.portal_user import PortalUserClient, PortalUserResponseModel
from src.api.clients.auth import AuthClient

from src.constants import ServerConfig
from src.logger import logger


app = FastAPI()

version = 1

GATEWAY_PATH = f"/api/v{version}"

team_client = TeamClient()
team_manager_client = TeamManagerClient()
player_client = PlayerClient()
referee_client = RefereeClient()
venue_client = VenueClient()
match_client = MatchClient()
championship_client = ChampionshipClient()
user_client = PortalUserClient()
auth_client = AuthClient()


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


@app.get('/google-auth-verify')
def google_auth_verify(id_token: Optional[str] = Header(None)):
    google_sub_id = auth_client.google_verify_id_token(id_token)
    if google_sub_id:
        return user_client.create_or_get_user_by_google_sub(google_sub_id)
    raise HTTPException(status_code=401, detail="ID Token is invalid")


@app.get(GATEWAY_PATH + '/healthcheck')
def healthcheck():
    return {"status": "ok"}


@app.get(GATEWAY_PATH + '/teams/{team_id}', response_model=TeamResponseModel)
def get_team(team_id):
    return team_client.get_team(team_id)


@app.get(GATEWAY_PATH + '/players/{player_id}', response_model=PlayerResponseModel)
def get_player(player_id):
    return player_client.get_player(player_id)


@app.get(GATEWAY_PATH + '/referees/{referee_id}', response_model=RefereeResponseModel)
def get_referee(referee_id):
    return referee_client.get_referee(referee_id)


@app.get(GATEWAY_PATH + '/venues/{venue_id}', response_model=VenueResponseModel)
def get_venue(venue_id):
    return venue_client.get_venue(venue_id)


@app.get(GATEWAY_PATH + '/matches/{match_id}', response_model=MatchResponseModel)
def get_match(match_id):
    return match_client.get_match(match_id)


@app.get(GATEWAY_PATH + '/team-managers/{team_manager_id}', response_model=TeamManagerResponseModel)
def get_team_manager(team_manager_id):
    return team_manager_client.get_team_manager(team_manager_id)


@app.get(GATEWAY_PATH + '/championships/{championship_id}', response_model=ChampionshipResponseModel)
def get_championship(championship_id):
    return championship_client.get_championship(championship_id)


def custom_openapi():
    ignore_routes = ["/", "/api/v1/healthcheck"]
    routes = [route for route in app.routes if route.path not in ignore_routes]
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="GAA API",
        version="1.0.0",
        description="GAA RESTful API documentation",
        routes=routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://stcomgalls.gaa.ie/wp-content/uploads/sites/30/2016/11/gaa-logo.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    logger.info(f"Starting app on port {ServerConfig.PORT}")
    uvicorn.run("run_server:app", host='0.0.0.0',
                port=ServerConfig.PORT,
                access_log=False)
