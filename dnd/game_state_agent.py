from google import genai
from game_state import GameState
from utils import format_prompt, GS_INITIAL_PROMPT

class GameStateAgent:
    def __init__(self, api_key, game_state: GameState):
        self.client = genai.Client(api_key=api_key)
        self.game_state = game_state
        
        config = {
            "tools": [game_state.add_history, game_state.add_player, game_state.add_location, game_state.add_npc,
                     game_state.update_player_state, game_state.update_npc_state, game_state.update_location_state,
                     game_state.get_player_state, game_state.get_location_state, game_state.get_npc_state,
                     game_state.get_all_players, game_state.get_all_npcs, game_state.get_all_locations, game_state.get_history],
        }

        self.chat = self.client.chats.create(model="gemini-2.0-flash", config=config)
        response = self.chat.send_message(GS_INITIAL_PROMPT)

    def update_game_state(self, dm_action):
        # Send DM action to the Game State agent
        prompt = format_prompt(dm_action) # See utils.py for formatting
        response = self.chat.send_message(prompt)
        return response.text