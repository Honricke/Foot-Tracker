from pydantic import BaseModel


class Matches:
    def __init__(self,*args):
        self.date: str = args[0]["date"]
        self.home_team: str = args[0]["home_team"]
        self.away_team: str = args[0]["away_team"]
        self.scoreboard: str = args[0]["scoreboard"]
        self.home_classification: int = args[0]["home_classification"]
        self.away_classification: int = args[0]["away_classification"]
        self.game_statistic: list[Statistic] = args[0]["game_statistic"]
        self.home_player_score: list[Rating] = args[0]["home_player_score"]
        self.away_player_score: list[Rating] = args[0]["away_player_score"]
        self.referee: str = args[0]["referee"]
        self.stadium: str = args[0]["stadium"]

class Rating(BaseModel):
    name: str
    score: str
    injurie: bool

class Statistic(BaseModel):
	description: str
	home_statistic: str
	away_statistic: str

	