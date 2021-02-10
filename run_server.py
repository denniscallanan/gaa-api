from typing import Optional

import uvicorn

from fastapi import FastAPI, Header, HTTPException
from fastapi.openapi.utils import get_openapi

from src.api.clients.base import db, BaseClient
from src.api.clients.team import *
from src.api.clients.team_manager import *
from src.api.clients.player import *
from src.api.clients.referee import *
from src.api.clients.venue import *
from src.api.clients.match import *
from src.api.clients.championship import *
from src.api.clients.portal_user import *
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
    return client.get_by_id(team_id, TeamTable).to_response_model(TeamRecord)


@app.get(GATEWAY_PATH + '/teams', response_model=TeamResponseModelList)
def search_teams(team_name: Optional[str] = None, main_venue_id: Optional[str] = None):
    records = [table.to_model(TeamRecord) for table in client.search_and_equal_conjunction(TeamTable, {
        TeamTable.team_name: team_name,
        TeamTable.main_venue_id: main_venue_id
    })]
    return TeamResponseModelList(status="success", result=records)


@app.post(GATEWAY_PATH + '/teams', response_model=TeamResponseModel)
def insert_team(team: Team, id_token: str = Header(None)):
    user = user_client.get_user_by_google_sub(auth_client.google_verify_id_token(id_token))
    if user:
        return client.insert(team, TeamTable, user).to_response_model(TeamRecord)
    raise HTTPException(status_code=401, detail=ResponseDetails.UNAUTHORIZED)


@app.put(GATEWAY_PATH + '/teams/{team_id}', response_model=TeamResponseModel)
def update_team(team_id, team: EditableTeam, id_token: str = Header(None)):
    user = user_client.get_user_by_google_sub(auth_client.google_verify_id_token(id_token))
    if user:
        return client.update(team_id, team, TeamTable, user).to_response_model(TeamRecord)
    raise HTTPException(status_code=401, detail=ResponseDetails.UNAUTHORIZED)


@app.get(GATEWAY_PATH + '/players/{player_id}', response_model=PlayerResponseModel)
def get_player(player_id):
    return client.get_by_id(player_id, PlayerTable).to_response_model(PlayerRecord)


@app.get(GATEWAY_PATH + '/players', response_model=PlayerResponseModelList)
def search_players(full_name: Optional[str] = None, team_id: Optional[str] = None):
    records = [table.to_model(PlayerRecord) for table in client.search_and_equal_conjunction(PlayerTable, {
        PlayerTable.full_name: full_name,
        PlayerTable.team_id: team_id
    })]
    return PlayerResponseModelList(status="success", result=records)


@app.post(GATEWAY_PATH + '/players', response_model=PlayerResponseModel)
def insert_player(player: Player, id_token: str = Header(None)):
    user = user_client.get_user_by_google_sub(auth_client.google_verify_id_token(id_token))
    if user:
        return client.insert(player, PlayerTable, user).to_response_model(PlayerRecord)
    raise HTTPException(status_code=401, detail=ResponseDetails.UNAUTHORIZED)


@app.put(GATEWAY_PATH + '/players/{player_id}', response_model=PlayerResponseModel)
def update_player(player_id, player: EditablePlayer, id_token: str = Header(None)):
    user = user_client.get_user_by_google_sub(auth_client.google_verify_id_token(id_token))
    if user:
        return client.update(player_id, player, PlayerTable, user).to_response_model(PlayerRecord)
    raise HTTPException(status_code=401, detail=ResponseDetails.UNAUTHORIZED)


@app.get(GATEWAY_PATH + '/referees/{referee_id}', response_model=RefereeResponseModel)
def get_referee(referee_id):
    return client.get_by_id(referee_id, RefereeTable).to_response_model(RefereeRecord)


@app.get(GATEWAY_PATH + '/referees', response_model=RefereeResponseModelList)
def search_referees(full_name: Optional[str] = None, county: Optional[str] = None):
    records = [table.to_model(RefereeRecord) for table in client.search_and_equal_conjunction(RefereeTable, {
        RefereeTable.full_name: full_name,
        RefereeTable.county: county
    })]
    return RefereeResponseModelList(status="success", result=records)


@app.post(GATEWAY_PATH + '/referees', response_model=RefereeResponseModel)
def insert_referee(referee: Referee, id_token: str = Header(None)):
    user = user_client.get_user_by_google_sub(auth_client.google_verify_id_token(id_token))
    if user:
        return client.insert(referee, RefereeTable, user).to_response_model(RefereeRecord)
    raise HTTPException(status_code=401, detail=ResponseDetails.UNAUTHORIZED)


@app.put(GATEWAY_PATH + '/referees/{referee_id}', response_model=RefereeResponseModel)
def update_referee(referee_id, referee: EditableReferee, id_token: str = Header(None)):
    user = user_client.get_user_by_google_sub(auth_client.google_verify_id_token(id_token))
    if user:
        return client.update(referee_id, referee, RefereeTable, user).to_response_model(RefereeRecord)
    raise HTTPException(status_code=401, detail=ResponseDetails.UNAUTHORIZED)


@app.get(GATEWAY_PATH + '/venues/{venue_id}', response_model=VenueResponseModel)
def get_venue(venue_id):
    return client.get_by_id(venue_id, VenueTable).to_response_model(VenueRecord)


@app.get(GATEWAY_PATH + '/venues', response_model=VenueResponseModelList)
def search_venues(venue_name: Optional[str] = None, venue_county: Optional[str] = None):
    records = [table.to_model(VenueRecord) for table in client.search_and_equal_conjunction(VenueTable, {
        VenueTable.venue_name: venue_name,
        VenueTable.venue_county: venue_county
    })]
    return VenueResponseModelList(status="success", result=records)


@app.post(GATEWAY_PATH + '/venues', response_model=VenueResponseModel)
def insert_venue(venue: Venue, id_token: str = Header(None)):
    user = user_client.get_user_by_google_sub(auth_client.google_verify_id_token(id_token))
    if user:
        return client.insert(venue, VenueTable, user).to_response_model(VenueRecord)
    raise HTTPException(status_code=401, detail=ResponseDetails.UNAUTHORIZED)


@app.put(GATEWAY_PATH + '/venues/{venue_id}', response_model=VenueResponseModel)
def update_venue(venue_id, venue: EditableVenue, id_token: str = Header(None)):
    user = user_client.get_user_by_google_sub(auth_client.google_verify_id_token(id_token))
    if user:
        return client.update(venue_id, venue, VenueTable, user).to_response_model(VenueRecord)
    raise HTTPException(status_code=401, detail=ResponseDetails.UNAUTHORIZED)


@app.get(GATEWAY_PATH + '/matches/{match_id}', response_model=MatchResponseModel)
def get_match(match_id):
    return client.get_by_id(match_id, MatchTable).to_response_model(MatchRecord)


@app.get(GATEWAY_PATH + '/matches', response_model=MatchResponseModelList)
def search_matches(away_team_id: Optional[str] = None, home_team_id: Optional[str] = None,
                   championship_id: Optional[str] = None, championship_round: Optional[str] = None, 
                   referee_id: Optional[str] = None):
    records = [table.to_model(MatchRecord) for table in client.search_and_equal_conjunction(MatchTable, {
        MatchTable.away_team_id: away_team_id,
        MatchTable.home_team_id: home_team_id,
        MatchTable.championship_id: championship_id,
        MatchTable.championship_round: championship_round,
        MatchTable.referee_id: referee_id,
    })]
    return MatchResponseModelList(status="success", result=records)


@app.post(GATEWAY_PATH + '/matches', response_model=MatchResponseModel)
def insert_match(match: Match, id_token: str = Header(None)):
    user = user_client.get_user_by_google_sub(auth_client.google_verify_id_token(id_token))
    if user:
        return client.insert(match, MatchTable, user).to_response_model(MatchRecord)
    raise HTTPException(status_code=401, detail=ResponseDetails.UNAUTHORIZED)


@app.put(GATEWAY_PATH + '/matches/{match_id}', response_model=MatchResponseModel)
def update_match(match_id, match: EditableMatch, id_token: str = Header(None)):
    user = user_client.get_user_by_google_sub(auth_client.google_verify_id_token(id_token))
    if user:
        return client.update(match_id, match, MatchTable, user).to_response_model(MatchRecord)
    raise HTTPException(status_code=401, detail=ResponseDetails.UNAUTHORIZED)


@app.get(GATEWAY_PATH + '/team-managers/{team_manager_id}', response_model=TeamManagerResponseModel)
def get_team_manager(team_manager_id):
    return client.get_by_id(team_manager_id, TeamManagerTable).to_response_model(TeamManagerRecord)


@app.get(GATEWAY_PATH + '/team-managers', response_model=TeamManagerResponseModelList)
def search_team_managers(full_name: Optional[str] = None, team_id: Optional[str] = None):
    records = [table.to_model(TeamManagerRecord) for table in client.search_and_equal_conjunction(TeamManagerTable, {
        TeamManagerTable.full_name: full_name,
        TeamManagerTable.team_id: team_id
    })]
    return TeamManagerResponseModelList(status="success", result=records)


@app.post(GATEWAY_PATH + '/team-managers', response_model=TeamManagerResponseModel)
def insert_team_manager(team_manager: TeamManager, id_token: str = Header(None)):
    user = user_client.get_user_by_google_sub(auth_client.google_verify_id_token(id_token))
    if user:
        return client.insert(team_manager, TeamManagerTable, user).to_response_model(TeamManagerRecord)
    raise HTTPException(status_code=401, detail=ResponseDetails.UNAUTHORIZED)


@app.put(GATEWAY_PATH + '/team-managers/{team_manager_id}', response_model=TeamManagerResponseModel)
def update_team_manager(team_manager_id, team_manager: EditableTeamManager, id_token: str = Header(None)):
    user = user_client.get_user_by_google_sub(auth_client.google_verify_id_token(id_token))
    if user:
        return client.update(team_manager_id, team_manager, TeamManagerTable, user).to_response_model(TeamManagerRecord)
    raise HTTPException(status_code=401, detail=ResponseDetails.UNAUTHORIZED)


@app.get(GATEWAY_PATH + '/championships/{championship_id}', response_model=ChampionshipResponseModel)
def get_championship(championship_id):
    return client.get_by_id(championship_id, ChampionshipTable).to_response_model(ChampionshipRecord)


@app.get(GATEWAY_PATH + '/championships', response_model=ChampionshipResponseModelList)
def search_championships(championship_name: Optional[str] = None):
    records = [table.to_model(ChampionshipRecord) for table in client.search_and_equal_conjunction(ChampionshipTable, {
        ChampionshipTable.championship_name: championship_name
    })]
    return ChampionshipResponseModelList(status="success", result=records)


@app.post(GATEWAY_PATH + '/championships', response_model=ChampionshipResponseModel)
def insert_championship(championship: Championship, id_token: str = Header(None)):
    user = user_client.get_user_by_google_sub(auth_client.google_verify_id_token(id_token))
    if user:
        return client.insert(championship, ChampionshipTable, user).to_response_model(ChampionshipRecord)
    raise HTTPException(status_code=401, detail=ResponseDetails.UNAUTHORIZED)


@app.put(GATEWAY_PATH + '/championships/{championship_id}', response_model=ChampionshipResponseModel)
def update_championship(championship_id, championship: EditableChampionship, id_token: str = Header(None)):
    user = user_client.get_user_by_google_sub(auth_client.google_verify_id_token(id_token))
    if user:
        return client.update(championship_id, championship, ChampionshipTable, user
                            ).to_response_model(ChampionshipRecord)
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
