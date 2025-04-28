from dm_agent import DM_Agent
from player_agent import PlayerAgent
from game_state import GameState

API_KEY = ''

class Game():
    def __init__(self, name: str):
        self.name = name
        self.players = []
        self.game_state = GameState()
        self.dm = DM_Agent(API_KEY, game_state=self.game_state)
        self.dm.start_game()
        self.game_checksum = 0

    def update_game_checksum(self):
        self.game_checksum = self.game_checksum + 1
        

    def add_player(self, player):
        self.players.append(player)
        self.update_game_checksum()


    def get_game_history(self):
        return self.game_state.get_history()
    
    def get_players_state(self):
        return self.game_state.get_all_players()
    
    def get_npcs_state(self):
        return self.game_state.get_all_npcs()
    
    def get_locations_state(self):
        return self.game_state.get_all_locations()
    
    def update_game(self, player_action):
        dm_response = self.dm.get_dm_response(player_action)
        self.game_state.add_history(dm_response)
        self.update_game_checksum()
        return dm_response

    def print_game_state(self):
        print("Game State:")
        self.game_state.print_state()

    def get_state_for_player(self, player_name):
        player_state = self.game_state.get_player_state(player_name)
        player_loc = player_state['location'] if player_state else "Unknown"
        player_location = self.game_state.get_location_state(player_loc)
        all_npcs = self.game_state.get_all_npcs()
        all_npcs_in_location = [npc for npc in all_npcs.values() if npc['location'] == player_loc]
        return {
            "player_state": player_state,
            "player_location": player_location,
            "all_npcs_in_location": all_npcs_in_location
        }

    def update_player(self, player_name, player_state):
        self.game_state.update_player_state(player_name, player_state)
        dm_response = self.dm.dm_message(f"Player {player_name} state updated.")
        self.game_state.add_history(dm_response)
        self.update_game_checksum()
        return dm_response

    def get_game_checksum(self):
        return self.game_checksum
