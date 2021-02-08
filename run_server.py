from typing import Optional

import uvicorn

from fastapi import FastAPI, Header, HTTPException
from fastapi.openapi.utils import get_openapi

from src.api.clients.base import db, BaseClient, DTO
from src.api.clients.team import TeamResponseModel, Team, TeamTable
from src.api.clients.team_manager import TeamManagerResponseModel, TeamManager, TeamManagerTable
from src.api.clients.player import PlayerResponseModel, Player, PlayerTable
from src.api.clients.referee import RefereeResponseModel, Referee, RefereeTable
from src.api.clients.venue import VenueResponseModel, Venue, VenueTable
from src.api.clients.match import MatchResponseModel, Match, MatchTable
from src.api.clients.championship import ChampionshipResponseModel, Championship, ChampionshipTable
from src.api.clients.portal_user import PortalUserClient, PortalUserResponseModel, PortalUser, PortalUserTable
from src.api.clients.auth import AuthClient

from src.constants import ServerConfig
from src.logger import logger


app = FastAPI()

version = 1

GATEWAY_PATH = f"/api/v{version}"

client = BaseClient()
user_client = PortalUserClient()
auth_client = AuthClient()


class ResponseDetails:
    UNAUTHORIZED = "You are unauthorized to make this request"

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
        return user_client.create_or_get_user_by_google_sub(google_sub_id).to_response_model(PortalUser)
    raise HTTPException(status_code=401, detail=ResponseDetails.UNAUTHORIZED)


@app.get(GATEWAY_PATH + '/healthcheck')
def healthcheck():
    return {"status": "ok"}


@app.get(GATEWAY_PATH + '/teams/{team_id}', response_model=TeamResponseModel)
def get_team(team_id):
    return client.get_by_id(team_id, TeamTable).to_response_model(Team)


@app.post(GATEWAY_PATH + '/teams', response_model=TeamResponseModel)
def insert_team(team: Team, id_token: Optional[str] = Header(None)):
    user = user_client.get_user_by_google_sub(auth_client.google_verify_id_token(id_token))
    if user:
        return client.insert(team, TeamTable, user).to_response_model(Team)
    raise HTTPException(status_code=401, detail=ResponseDetails.UNAUTHORIZED)


@app.put(GATEWAY_PATH + '/teams/{team_id}', response_model=TeamResponseModel)
def update_team(team_id, team: Team.get_editable_model(), id_token: Optional[str] = Header(None)):
    user = user_client.get_user_by_google_sub(auth_client.google_verify_id_token(id_token))
    if user:
        return client.update(team_id, team, TeamTable, user).to_response_model(Team)
    raise HTTPException(status_code=401, detail=ResponseDetails.UNAUTHORIZED)


@app.get(GATEWAY_PATH + '/players/{player_id}', response_model=PlayerResponseModel)
def get_player(player_id):
    return client.get_by_id(player_id, PlayerTable).to_response_model(Player)


@app.post(GATEWAY_PATH + '/players', response_model=PlayerResponseModel)
def insert_player(player: Player, id_token: Optional[str] = Header(None)):
    user = user_client.get_user_by_google_sub(auth_client.google_verify_id_token(id_token))
    if user:
        return client.insert(player, PlayerTable, user).to_response_model(Player)
    raise HTTPException(status_code=401, detail=ResponseDetails.UNAUTHORIZED)


@app.put(GATEWAY_PATH + '/players/{player_id}', response_model=PlayerResponseModel)
def update_player(player_id, player: Player, id_token: Optional[str] = Header(None)):
    user = user_client.get_user_by_google_sub(auth_client.google_verify_id_token(id_token))
    if user:
        return client.update(player_id, player, PlayerTable, user).to_response_model(Player)
    raise HTTPException(status_code=401, detail=ResponseDetails.UNAUTHORIZED)


@app.get(GATEWAY_PATH + '/referees/{referee_id}', response_model=RefereeResponseModel)
def get_referee(referee_id):
    return client.get_by_id(referee_id, RefereeTable).to_response_model(Referee)


@app.post(GATEWAY_PATH + '/referees', response_model=RefereeResponseModel)
def insert_referee(referee: Team, id_token: Optional[str] = Header(None)):
    user = user_client.get_user_by_google_sub(auth_client.google_verify_id_token(id_token))
    if user:
        return client.insert(referee, RefereeTable, user).to_response_model(Referee)
    raise HTTPException(status_code=401, detail=ResponseDetails.UNAUTHORIZED)


@app.put(GATEWAY_PATH + '/referees/{referee_id}', response_model=RefereeResponseModel)
def update_referee(referee_id, referee: Referee, id_token: Optional[str] = Header(None)):
    user = user_client.get_user_by_google_sub(auth_client.google_verify_id_token(id_token))
    if user:
        return client.update(referee_id, referee, RefereeTable, user).to_response_model(Referee)
    raise HTTPException(status_code=401, detail=ResponseDetails.UNAUTHORIZED)


@app.get(GATEWAY_PATH + '/venues/{venue_id}', response_model=VenueResponseModel)
def get_venue(venue_id):
    return client.get_by_id(venue_id, VenueTable).to_response_model(Venue)


@app.post(GATEWAY_PATH + '/venues', response_model=VenueResponseModel)
def insert_venue(venue: Venue, id_token: Optional[str] = Header(None)):
    user = user_client.get_user_by_google_sub(auth_client.google_verify_id_token(id_token))
    if user:
        return client.insert(venue, VenueTable, user).to_response_model(Venue)
    raise HTTPException(status_code=401, detail=ResponseDetails.UNAUTHORIZED)


@app.put(GATEWAY_PATH + '/venues/{venue_id}', response_model=VenueResponseModel)
def update_venue(venue_id, venue: Venue, id_token: Optional[str] = Header(None)):
    user = user_client.get_user_by_google_sub(auth_client.google_verify_id_token(id_token))
    if user:
        return client.update(venue_id, venue, VenueTable, user).to_response_model(Venue)
    raise HTTPException(status_code=401, detail=ResponseDetails.UNAUTHORIZED)


@app.get(GATEWAY_PATH + '/matches/{match_id}', response_model=MatchResponseModel)
def get_match(match_id):
    return client.get_by_id(match_id, MatchTable).to_response_model(Match)


@app.post(GATEWAY_PATH + '/matches', response_model=MatchResponseModel)
def insert_match(match: Match, id_token: Optional[str] = Header(None)):
    user = user_client.get_user_by_google_sub(auth_client.google_verify_id_token(id_token))
    if user:
        return client.insert(match, MatchTable, user).to_response_model(Match)
    raise HTTPException(status_code=401, detail=ResponseDetails.UNAUTHORIZED)


@app.put(GATEWAY_PATH + '/matches/{match_id}', response_model=MatchResponseModel)
def update_match(match_id, match: Match, id_token: Optional[str] = Header(None)):
    user = user_client.get_user_by_google_sub(auth_client.google_verify_id_token(id_token))
    if user:
        return client.update(match_id, match, MatchTable, user).to_response_model(Match)
    raise HTTPException(status_code=401, detail=ResponseDetails.UNAUTHORIZED)


@app.get(GATEWAY_PATH + '/team-managers/{team_manager_id}', response_model=TeamManagerResponseModel)
def get_team_manager(team_manager_id):
    return client.get_by_id(team_manager_id, TeamManagerTable).to_response_model(TeamManager)


@app.post(GATEWAY_PATH + '/team-managers', response_model=TeamManagerResponseModel)
def insert_team_manager(team_manager: TeamManager, id_token: Optional[str] = Header(None)):
    user = user_client.get_user_by_google_sub(auth_client.google_verify_id_token(id_token))
    if user:
        return client.insert(team_manager, TeamManagerTable, user).to_response_model(TeamManager)
    raise HTTPException(status_code=401, detail=ResponseDetails.UNAUTHORIZED)


@app.put(GATEWAY_PATH + '/team-managers/{team_manager_id}', response_model=TeamManagerResponseModel)
def update_team_manager(team_manager_id, team_manager: TeamManager, id_token: Optional[str] = Header(None)):
    user = user_client.get_user_by_google_sub(auth_client.google_verify_id_token(id_token))
    if user:
        return client.update(team_manager_id, team_manager, TeamManagerTable, user).to_response_model(TeamManager)
    raise HTTPException(status_code=401, detail=ResponseDetails.UNAUTHORIZED)


@app.get(GATEWAY_PATH + '/championships/{championship_id}', response_model=ChampionshipResponseModel)
def get_championship(championship_id):
    return client.get_by_id(championship_id, ChampionshipTable).to_response_model(Championship)


@app.post(GATEWAY_PATH + '/championships', response_model=ChampionshipResponseModel)
def insert_championship(championship: Championship, id_token: Optional[str] = Header(None)):
    user = user_client.get_user_by_google_sub(auth_client.google_verify_id_token(id_token))
    if user:
        return client.insert(championship, ChampionshipTable, user).to_response_model(Championship)
    raise HTTPException(status_code=401, detail=ResponseDetails.UNAUTHORIZED)


@app.put(GATEWAY_PATH + '/championships/{championship_id}', response_model=ChampionshipResponseModel)
def update_championship(championship_id, championship: Championship, id_token: Optional[str] = Header(None)):
    user = user_client.get_user_by_google_sub(auth_client.google_verify_id_token(id_token))
    if user:
        return client.update(championship_id, championship, ChampionshipTable, user).to_response_model(Championship)
    raise HTTPException(status_code=401, detail=ResponseDetails.UNAUTHORIZED)


@app.get(GATEWAY_PATH + '/users/{user_id}', response_model=PortalUserResponseModel)
def get_user(user_id):
    return client.get_by_id(user_id, PortalUserTable).to_response_model(PortalUser)


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
