from src.DirectRequest import Request
from src.db_queries import save_match_data, get_last_date
import json

class Main:
    def __init__(self):
        self.request = Request()

    def start(self):
        # last_date = get_last_date()
        last_date = "01/09/24"

        self.request.open_browser()
        self.request.open_site()
        games = self.request.get_link_by_date(last_date)

        games_data = []

        for game in games:
            game_data = self.request.get_game_data(game)
            games_data.append(game_data)
            save_match_data(game_data)

Main().start()