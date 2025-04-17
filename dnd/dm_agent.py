from google import genai
from utils import format_prompt, INITIAL_PROMPT, GAME_START_PROMPT
from game_state import GameState

class DM_Agent:
    def __init__(self, api_key, game_state: GameState):
        self.client = genai.Client(api_key=api_key)
        self.game_state = game_state
        
        config = {
            "tools": [game_state.add_history, game_state.add_player, game_state.add_location, game_state.add_npc,
                     game_state.update_player_state, game_state.update_npc_state, game_state.update_location_state,
                     game_state.get_player_state, game_state.get_location_state, game_state.get_npc_state,
                     game_state.get_all_players, game_state.get_all_npcs, game_state.get_all_locations, game_state.get_history, 
                     game_state.roll_dice],
        }

        self.chat = self.client.chats.create(model="gemini-2.0-flash", config=config)
        response = self.chat.send_message(INITIAL_PROMPT)

        print("\nDUNGEONS & DRAGONS")

        response = self.chat.send_message(GAME_START_PROMPT)
        response = print(response.text)

    def set_game_state(self, game_state):
        self.game_state = game_state

    def get_dm_response(self, player_action):
        # Send player action to the DM agent
        prompt = format_prompt(player_action) # See utils.py for formatting
        response = self.chat.send_message(prompt)
        return response.text
    
    def get_dm_overview(self):
        # Get the current state of the game from the DM agent
        return self.chat.send_message("Story tell me the game state right now").text
    