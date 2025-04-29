import logging
from google import genai
from utils import format_prompt, DM_INITIAL_PROMPT
from game_state import GameState

logger = logging.getLogger(__name__)

class DM_Agent:
    def __init__(self, api_key, game_state: GameState):
        try:
            logger.info("Initializing DM_Agent")
            self.client = genai.Client(api_key=api_key)
            self.game_state = game_state
            
            config = {
                "tools": [game_state.add_player, game_state.add_location, game_state.add_npc,
                         game_state.update_player_state, game_state.update_npc_state, game_state.update_location_state,
                         game_state.get_player_state, game_state.get_location_state, game_state.get_npc_state,
                         game_state.get_all_players, game_state.get_all_npcs, game_state.get_all_locations, game_state.get_history],
            }

            self.chat = self.client.chats.create(model="gemini-2.0-flash", config=config)
            logger.info("Successfully initialized DM_Agent")
        except Exception as e:
            logger.error(f"Error initializing DM_Agent: {str(e)}", exc_info=True)
            raise

    def set_game_state(self, game_state):
        try:
            logger.info("Setting new game state")
            self.game_state = game_state
            logger.info("Successfully set new game state")
        except Exception as e:
            logger.error(f"Error setting game state: {str(e)}", exc_info=True)
            raise

    def get_dm_response(self, player_action):
        try:
            logger.info(f"Getting DM response for player action: {player_action}")
            prompt = format_prompt(player_action)
            response = self.chat.send_message(prompt)
            logger.info("Successfully received DM response")
            return response.text
        except Exception as e:
            logger.error(f"Error getting DM response: {str(e)}", exc_info=True)
            raise
    
    def dm_message(self, message):
        try:
            logger.info(f"Sending DM message: {message}")
            response = self.chat.send_message(message)
            logger.info("Successfully sent DM message")
            return response.text
        except Exception as e:
            logger.error(f"Error sending DM message: {str(e)}", exc_info=True)
            raise
    
