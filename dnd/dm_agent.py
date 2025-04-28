from google import genai
from utils import format_prompt, DM_INITIAL_PROMPT, GAME_START_PROMPT
from game_state import GameState

class DM_Agent:
    def __init__(self, api_key, game_state: GameState):
        self.client = genai.Client(api_key=api_key)
        self.game_state = game_state
        
        config = {
            "tools": [game_state.add_player, game_state.add_location, game_state.add_npc,
                     game_state.update_player_state, game_state.update_npc_state, game_state.update_location_state,
                     game_state.get_player_state, game_state.get_location_state, game_state.get_npc_state,
                     game_state.get_all_players, game_state.get_all_npcs, game_state.get_all_locations, game_state.get_history],
        }

        self.chat = self.client.chats.create(model="gemini-2.5-flash-preview-04-17", config=config)

    def start_game(self):
        response = self.chat.send_message(INITIAL_PROMPT)

        print("\nDUNGEONS & DRAGONS")

    def start_game(self):
        response = self.chat.send_message(GAME_START_PROMPT)
        print(response.text)
        self.game_state.add_history(response.text)

    def set_game_state(self, game_state):
        self.game_state = game_state

    def get_dm_response(self, player_action):
        # Send player action to the DM agent
        prompt = format_prompt(player_action) # See utils.py for formatting
        response = self.chat.send_message(prompt)
        return response.text
    
    def dm_message(self, message):
        response = self.chat.send_message(message)
        return response.text
    
