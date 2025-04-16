from game_state import GameState
from dm_agent import DM_Agent
from player_agent import PlayerAgent
import os
import re

# Replace with your actual API key
API_KEY = ''
game_state = GameState()

dm = DM_Agent(API_KEY, game_state=game_state)
player = PlayerAgent("")

while True:
    player_action = player.get_player_action()
    dm_response = dm.get_dm_response(player_action)
    print(f"DM Response: {dm_response}")
    game_state.print_state()
    print(dm.get_dm_overview())

   