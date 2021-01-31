

TEAM_ID = "teamID"
TEAM_NAME = "teamName"
SPORT = "sport"
ESTABLISHED_YEAR = "estYear"

class Team:

    def __init__(self, team_id, team_name, sport, est_year, is_county):
        self.team_id = team_id
        self.team_name = team_name
        self.sport = sport
        self.est_year = est_year
        self.is_county = is_county

    @staticmethod
    def from_record(*args):
        return Team(None, *args)

    def to_dict(self):
        return {
            TEAM_ID: self.team_id,
            TEAM_NAME: self.team_name,
            SPORT: self.sport,
            ESTABLISHED_YEAR: self.est_year
        }


class TeamClient:

    def __init__(self, conn):
        self.conn = conn

    def get_team(self, team_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT team_name, sport, est_year, is_county FROM team WHERE team_id = %s", team_id)
        team = Team.from_record(*cursor.fetchone())
        return team.to_dict()
