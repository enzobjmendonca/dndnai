import logging
from utils import DICE_PATTERN
from data.player import Player
from data.npc import Npc
from data.location import Location

logger = logging.getLogger(__name__)

class GameState:
    def __init__(self, debug = False):
        self.players = {}
        self.locations = {}
        self.npcs = {}
        self.history = []
        self.current_location = None
        self.debug = debug
        logger.info("Initialized new GameState instance")

    def add_player(self, player_name: str) -> bool:
        try:
            logger.info(f"Attempting to add player: {player_name}")
            if player_name not in self.players:
                self.players[player_name] = Player(player_name)
                logger.info(f"Successfully added player: {player_name}")
                return True
            else:
                logger.warning(f"Player {player_name} already exists in game state")
                return False
        except Exception as e:
            logger.error(f"Error adding player {player_name}: {str(e)}", exc_info=True)
            return False

    def get_player_state(self, player_name: str) -> dict:
        try:
            logger.info(f"Retrieving state for player: {player_name}")
            if player_name in self.players:
                state = self.players[player_name].to_dict()
                logger.info(f"Successfully retrieved state for player: {player_name}")
                return state
            else:
                logger.warning(f"Player {player_name} not found in game state")
                return None
        except Exception as e:
            logger.error(f"Error retrieving state for player {player_name}: {str(e)}", exc_info=True)
            return None

    def update_player_state(self, player_name: str, new_state: dict) -> bool:
        try:
            logger.info(f"Updating state for player: {player_name}")
            if player_name in self.players:
                current_state_dict = self.players[player_name].to_dict()
                current_state_dict.update(new_state)
                self.players[player_name].from_dict(current_state_dict)
                logger.info(f"Successfully updated state for player: {player_name}")
                return True
            else:
                logger.warning(f"Player {player_name} not found in game state")
                return False
        except Exception as e:
            logger.error(f"Error updating state for player {player_name}: {str(e)}", exc_info=True)
            return False
    
    def add_location(self, location_name: str, description: str) -> bool:
        try:
            logger.info(f"Attempting to add location: {location_name}")
            if location_name not in self.locations:
                self.locations[location_name] = Location(location_name, description)
                logger.info(f"Successfully added location: {location_name}")
                return True
            else:
                logger.warning(f"Location {location_name} already exists in game state")
                return False
        except Exception as e:
            logger.error(f"Error adding location {location_name}: {str(e)}", exc_info=True)
            return False

    def get_location_state(self, location_name: str) -> dict:
        try:
            logger.info(f"Retrieving state for location: {location_name}")
            if location_name in self.locations:
                state = self.locations[location_name].to_dict()
                logger.info(f"Successfully retrieved state for location: {location_name}")
                return state
            else:
                logger.warning(f"Location {location_name} not found in game state")
                return None
        except Exception as e:
            logger.error(f"Error retrieving state for location {location_name}: {str(e)}", exc_info=True)
            return None
    
    def update_location_state(self, location_name: str, new_state: dict) -> bool:
        try:
            logger.info(f"Updating state for location: {location_name}")
            if location_name in self.locations:
                current_state_dict = self.locations[location_name].to_dict()
                current_state_dict.update(new_state)
                self.locations[location_name].from_dict(current_state_dict)
                logger.info(f"Successfully updated state for location: {location_name}")
                return True
            else:
                self.locations[location_name] = Location(location_name).from_dict(new_state)
                logger.info(f"Created new location: {location_name}")
                return True
        except Exception as e:
            logger.error(f"Error updating state for location {location_name}: {str(e)}", exc_info=True)
            return False
        
    def add_npc(self, npc_name: str) -> bool:
        try:
            logger.info(f"Attempting to add NPC: {npc_name}")
            if npc_name not in self.npcs:
                self.npcs[npc_name] = Npc(npc_name)
                logger.info(f"Successfully added NPC: {npc_name}")
                return True
            else:
                logger.warning(f"NPC {npc_name} already exists in game state")
                return False
        except Exception as e:
            logger.error(f"Error adding NPC {npc_name}: {str(e)}", exc_info=True)
            return False

    def get_npc_state(self, npc_name: str) -> dict:
        try:
            logger.info(f"Retrieving state for NPC: {npc_name}")
            if npc_name in self.npcs:
                state = self.npcs[npc_name].to_dict()
                logger.info(f"Successfully retrieved state for NPC: {npc_name}")
                return state
            else:
                logger.warning(f"NPC {npc_name} not found in game state")
                return None
        except Exception as e:
            logger.error(f"Error retrieving state for NPC {npc_name}: {str(e)}", exc_info=True)
            return None

    def update_npc_state(self, npc_name: str, new_state: dict) -> bool:
        try:
            logger.info(f"Updating state for NPC: {npc_name}")
            if npc_name in self.npcs:
                current_state_dict = self.npcs[npc_name].to_dict()
                current_state_dict.update(new_state)
                self.npcs[npc_name].from_dict(current_state_dict)
                logger.info(f"Successfully updated state for NPC: {npc_name}")
                return True
            else:
                logger.warning(f"NPC {npc_name} not found in game state")
                return False
        except Exception as e:
            logger.error(f"Error updating state for NPC {npc_name}: {str(e)}", exc_info=True)
            return False
    
    def add_history(self, log_entry: str) -> None:
        try:
            logger.info(f"Adding entry to game history: {log_entry}")
            self.history.append(log_entry)
            logger.info("Successfully added entry to game history")
        except Exception as e:
            logger.error(f"Error adding entry to game history: {str(e)}", exc_info=True)

    def get_all_players(self) -> dict:
        try:
            logger.info("Retrieving all players")
            player_dict = {}
            for player in self.players.keys():
                player_dict[player] = self.players[player].to_dict()
            logger.info("Successfully retrieved all players")
            return player_dict
        except Exception as e:
            logger.error(f"Error retrieving all players: {str(e)}", exc_info=True)
            return {}

    def get_all_npcs(self) -> dict:
        try:
            logger.info("Retrieving all NPCs")
            npc_dict = {}
            for npc in self.npcs.keys():
                npc_dict[npc] = self.npcs[npc].to_dict()
            logger.info("Successfully retrieved all NPCs")
            return npc_dict
        except Exception as e:
            logger.error(f"Error retrieving all NPCs: {str(e)}", exc_info=True)
            return {}

    def get_all_locations(self) -> dict:
        try:
            logger.info("Retrieving all locations")
            location_dict = {}
            for location in self.locations.keys():
                location_dict[location] = self.locations[location].to_dict()
            logger.info("Successfully retrieved all locations")
            return location_dict
        except Exception as e:
            logger.error(f"Error retrieving all locations: {str(e)}", exc_info=True)
            return {}

    def get_history(self) -> list:
        try:
            logger.info("Retrieving game history")
            history = self.history.copy()
            logger.info("Successfully retrieved game history")
            return history
        except Exception as e:
            logger.error(f"Error retrieving game history: {str(e)}", exc_info=True)
            return []

    def print_state(self) -> None:
        try:
            logger.info("Printing game state")
            print("Game State:")
            print(f"Players: {self.players}")
            print(f"Locations: {self.locations}")
            print(f"NPCs: {self.npcs}")
            print(f"Current Location: {self.current_location}")
            logger.info("Successfully printed game state")
        except Exception as e:
            logger.error(f"Error printing game state: {str(e)}", exc_info=True)