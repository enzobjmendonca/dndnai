import logging
from dm_agent import DM_Agent
from player_agent import PlayerAgent
from game_state import GameState
import os

logger = logging.getLogger(__name__)

API_KEY = os.getenv('API_KEY', '')
if not API_KEY:
    logger.warning("API_KEY not found in environment variables")

class Game():
    def __init__(self, name: str):
        try:
            logger.info(f"Initializing new game: {name}")
            self.name = name
            self.players = []
            self.game_state = GameState()
            print(API_KEY)
            self.dm = DM_Agent(API_KEY, game_state=self.game_state)
            self.game_checksum = 0
            logger.info(f"Successfully initialized game: {name}")
        except Exception as e:
            logger.error(f"Error initializing game {name}: {str(e)}", exc_info=True)
            raise

    def update_game_checksum(self):
        try:
            logger.info("Updating game checksum")
            self.game_checksum = self.game_checksum + 1
            logger.info(f"Successfully updated game checksum to: {self.game_checksum}")
        except Exception as e:
            logger.error(f"Error updating game checksum: {str(e)}", exc_info=True)
            raise

    def add_player(self, player):
        try:
            logger.info(f"Adding player: {player}")
            self.players.append(player)
            self.update_game_checksum()
            logger.info(f"Successfully added player: {player}")
        except Exception as e:
            logger.error(f"Error adding player {player}: {str(e)}", exc_info=True)
            raise

    def get_game_history(self):
        try:
            logger.info("Retrieving game history")
            history = self.game_state.get_history()
            logger.info("Successfully retrieved game history")
            return history
        except Exception as e:
            logger.error(f"Error retrieving game history: {str(e)}", exc_info=True)
            raise
    
    def get_players_state(self):
        try:
            logger.info("Retrieving players state")
            state = self.game_state.get_all_players()
            logger.info("Successfully retrieved players state")
            return state
        except Exception as e:
            logger.error(f"Error retrieving players state: {str(e)}", exc_info=True)
            raise
    
    def get_npcs_state(self):
        try:
            logger.info("Retrieving NPCs state")
            state = self.game_state.get_all_npcs()
            logger.info("Successfully retrieved NPCs state")
            return state
        except Exception as e:
            logger.error(f"Error retrieving NPCs state: {str(e)}", exc_info=True)
            raise
    
    def get_locations_state(self):
        try:
            logger.info("Retrieving locations state")
            state = self.game_state.get_all_locations()
            logger.info("Successfully retrieved locations state")
            return state
        except Exception as e:
            logger.error(f"Error retrieving locations state: {str(e)}", exc_info=True)
            raise
    
    def update_game(self, player_action):
        try:
            logger.info(f"Updating game with player action: {player_action}")
            dm_response = self.dm.get_dm_response(player_action)
            self.game_state.add_history(dm_response)
            self.update_game_checksum()
            logger.info("Successfully updated game")
            return dm_response
        except Exception as e:
            logger.error(f"Error updating game: {str(e)}", exc_info=True)
            raise

    def print_game_state(self):
        try:
            logger.info("Printing game state")
            print("Game State:")
            self.game_state.print_state()
            logger.info("Successfully printed game state")
        except Exception as e:
            logger.error(f"Error printing game state: {str(e)}", exc_info=True)
            raise

    def get_state_for_player(self, player_name):
        try:
            logger.info(f"Getting state for player: {player_name}")
            player_state = self.game_state.get_player_state(player_name)
            player_loc = player_state['location'] if player_state else "Unknown"
            player_location = self.game_state.get_location_state(player_loc)
            all_npcs = self.game_state.get_all_npcs()
            all_npcs_in_location = [npc for npc in all_npcs.values() if npc['location'] == player_loc]
            state = {
                "player_state": player_state,
                "player_location": player_location,
                "all_npcs_in_location": all_npcs_in_location
            }
            logger.info(f"Successfully retrieved state for player: {player_name}")
            return state
        except Exception as e:
            logger.error(f"Error getting state for player {player_name}: {str(e)}", exc_info=True)
            raise

    def update_player(self, player_name, player_state):
        try:
            logger.info(f"Updating player {player_name} with new state")
            self.game_state.update_player_state(player_name, player_state)
            dm_response = self.dm.dm_message(f"Player {player_name} state updated.")
            self.game_state.add_history(dm_response)
            self.update_game_checksum()
            logger.info(f"Successfully updated player {player_name}")
            return dm_response
        except Exception as e:
            logger.error(f"Error updating player {player_name}: {str(e)}", exc_info=True)
            raise

    def get_game_checksum(self):
        try:
            checksum = self.game_checksum
            return checksum
        except Exception as e:
            logger.error(f"Error getting game checksum: {str(e)}", exc_info=True)
            raise
