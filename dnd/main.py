from game_state import GameState
from dm_agent import DM_Agent
from player_agent import PlayerAgent
from game_state_agent import GameStateAgent

# Replace with your actual API key
API_KEY = ''
game_state = GameState()

dm = DM_Agent(API_KEY, game_state=game_state)
gs_agent = GameStateAgent(API_KEY, game_state=game_state)
gs_agent.update_game_state("This is the initial game state, plase populate and create all locations and npcs described here: " + dm.start_game())
player = PlayerAgent("")

while True:
    player_action = player.get_player_action()
    dm_response = dm.get_dm_response(player_action)
    print(f"DM Response: {dm_response}")
    gs_agent_response = gs_agent.update_game_state(dm_response)
    print(f"Game State Agent Response: {gs_agent_response}")
    game_state.print_state()
    #print(dm.get_dm_overview())

   