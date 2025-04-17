from utils import DICE_PATTERN
from data.player import Player
from data.npc import Npc
from data.location import Location


class GameState:
    def __init__(self, debug = False):
        self.players = {}
        self.locations = {}
        self.npcs = {}
        self.history = []
        self.current_location = None
        self.debug = debug


    def add_player(self, player_name: str) -> bool:
        """
        Adds a new player to the game state.

        Args:
            player_name (str): The name of the player to add.

        Behavior:
            - If the player does not already exist in the game state, a new Player
              instance is created and added to the `players` dictionary with the
              player's name as the key.
            - If the player already exists, a message is printed indicating that
              the player is already in the game state.
        
        Returns: 
            bool: True if the player was added successfully, False if the player already exists.
        """
        if self.debug:
            print(f"Adding player: {player_name}")
        if player_name not in self.players:
            self.players[player_name] = Player(player_name)
            return True
        else:
            return False

    def get_player_state(self, player_name: str) -> dict:
        """
        Retrieve the state of a specific player by their name.

        Args:
            player_name (str): The name of the player whose state is to be retrieved.

        Returns:
            dict or None: The state of the player as a dictionary if the player exists,
                          otherwise None.
        """
        if self.debug:
            print(f"Getting state for player: {player_name}")
        return self.players[player_name].to_dict() if player_name in self.players else None

    def update_player_state(self, player_name: str, new_state: dict) -> bool:
        """
        Updates the state of a specified player in the game.

        Args:
            player_name (str): The name of the player whose state is to be updated.
            new_state (dict): A dictionary with the new state of the player.

        Returns:
            bool: True if the player state was updated successfully, False otherwise.

        Prints:
            A message if the specified player is not found in the game state.
        """
        if self.debug:
            print(f"Updating state for player: {player_name} => {new_state}")
        if player_name in self.players:
            current_state_dict = self.players[player_name].to_dict()
            current_state_dict.update(new_state)
            self.players[player_name].from_dict(current_state_dict)
            return True
        else:
            if self.debug:
                print('Player not found in game state.')
            return False
    
    def add_location(self, location_name: str, description: str) -> bool:
        """
        Adds a new location to the game state.
        Args:
            location_name (str): The name of the location to add.
            description (str): A brief description of the location.
        Behavior:
            - If the location does not already exist in the game state, it creates a new
              Location object and adds it to the `locations` dictionary.
            - If the location already exists, it prints a message indicating that the
              location is already present.
        Note:
            The `locations` attribute is expected to be a dictionary where keys are
            location names and values are `Location` objects.
        Returns:
            bool: True if the location was added successfully, False if the location already exists.
        """
        if self.debug:
            print(f"Adding location: {location_name}")
        if location_name not in self.locations:
            self.locations[location_name] = Location(location_name, description)
            return True
        else:
            if self.debug:
                print('Location already exists in game state.')
            return False

    def get_location_state(self, location_name: str) -> dict:
        """
        Retrieve the state of a specified location as a dictionary.

        Args:
            location_name (str): The name of the location to retrieve.

        Returns:
            dict: A dictionary representation of the location's state if the location exists.
            None: If the specified location does not exist.
        """
        if self.debug:
            print(f"Getting state for location: {location_name}")
        return self.locations[location_name].to_dict() if location_name in self.locations else None
    
    def update_location_state(self, location_name: str, new_state: dict) -> bool:
        """
        Updates the state of a specified location. If the location does not exist,
        it creates a new location with the given state.
        Args:
            location_name (str): The name of the location to update or create.
            new_state (dict): A dictionary representing the new state of the location.
        Raises:
            KeyError: If the location_name is invalid or cannot be processed.
        Returns: 
            bool: True if the location state was updated successfully, False otherwise.
        """
        if self.debug:
            print(f"Updating state for location: {location_name} => {new_state}")
        if location_name in self.locations:
            current_state_dict = self.locations[location_name].to_dict()
            current_state_dict.update(new_state)
            self.locations[location_name].from_dict(current_state_dict)
            return True
        else:
            self.locations[location_name] = Location(location_name).from_dict(new_state)
            return False
        
    def add_npc(self, npc_name: str) -> bool:
        """
        Adds a new npc to the game state.

        Args:
            npc_name (str): The name of the npc to add.

        Behavior:
            - If the npc does not already exist in the game state, a new Npc
              instance is created and added to the `npcs` dictionary with the
              npc's name as the key.
            - If the npc already exists, a message is printed indicating that
              the npc is already in the game state.
        
        Returns: 
            bool: True if the npc was added successfully, False if the npc already exists.
        """
        if self.debug:
            print(f"Adding npc: {npc_name}")
        if npc_name not in self.npcs:
            self.npcs[npc_name] = Npc(npc_name)
            return True
        else:
            return False

    def get_npc_state(self, npc_name: str) -> dict:
        """
        Retrieve the state of a specific npc by their name.

        Args:
            npc_name (str): The name of the npc whose state is to be retrieved.

        Returns:
            dict or None: The state of the npc as a dictionary if the npc exists,
                          otherwise None.
        """
        if self.debug:
            print(f"Getting state for npc: {npc_name}")
        return self.npcs[npc_name].to_dict() if npc_name in self.npcs else None

    def update_npc_state(self, npc_name: str, new_state: dict) -> bool:
        """
        Updates the state of a specified npc in the game.

        Args:
            npc_name (str): The name of the npc whose state is to be updated.
            new_state (dict): A dictionary with the new state of the npc.

        Returns:
            bool: True if the npc state was updated successfully, False otherwise.

        Prints:
            A message if the specified npc is not found in the game state.
        """
        if self.debug:
            print(f"Updating state for npc: {npc_name} => {new_state}")
        if npc_name in self.npcs:
            current_state_dict = self.npcs[npc_name].to_dict()
            current_state_dict.update(new_state)
            self.npcs[npc_name].from_dict(current_state_dict)
            return True
        else:
            if self.debug:
                print('Npc not found in game state.')
            return False
    
    def add_history(self, action: str) -> None:
        """
        Adds an action to the game history.

        Args:
            action (str): The action to be added to the history.
        """
        if self.debug:
            print(f"Adding action to history: {action}")
        self.history.append(action)
    
    def roll_dice(dice_string: str) -> int:
        """
        Rolls dice based on standard D&D notation string.

        Args:
            dice_string: A string representing the dice roll (e.g., "d20", "2d6", "1d8+4", "3d10-1").
                        Whitespace around components is ignored. Case-insensitive 'd'.

        Returns:
            The integer result of the dice roll.

        Raises:
            ValueError: If the dice_string format is invalid or sides are non-positive.
        """
        dice_string = dice_string.lower().strip()
        match = DICE_PATTERN.match(dice_string)

        if not match:
            raise ValueError(f"Invalid dice string format: '{dice_string}'")

        num_dice_str, sides_str, operator, modifier_str = match.groups()

        # Determine the number of dice (default to 1 if not specified)
        num_dice = int(num_dice_str) if num_dice_str else 1

        # Determine the number of sides
        try:
            sides = int(sides_str)
            if sides <= 0:
                raise ValueError("Number of sides must be positive.")
        except ValueError:
            raise ValueError(f"Invalid number of sides: '{sides_str}'")

        # Determine the modifier (default to 0 if not specified)
        modifier = 0
        if operator and modifier_str:
            try:
                mod_value = int(modifier_str)
                if operator == '-':
                    modifier = -mod_value
                else: # operator == '+'
                    modifier = mod_value
            except ValueError:
                raise ValueError(f"Invalid modifier value: '{modifier_str}'")

        # --- Perform the rolls ---
        total_roll = 0
        individual_rolls = [] # Keep track for logging/debugging if needed

        if num_dice <= 0:
            print(f"Attempted to roll zero or negative dice ({num_dice}). Resulting in 0 base roll.")
            # Continue to just add the modifier if applicable
        else:
            for _ in range(num_dice):
                roll = int(input(f"Roll a d{sides}: "))
                individual_rolls.append(roll)
                total_roll += roll

        final_result = total_roll + modifier

        # Log the detailed roll
        roll_details = f"{num_dice}d{sides}"
        if modifier > 0:
            roll_details += f"+{modifier}"
        elif modifier < 0:
            roll_details += f"{modifier}" # Sign is already included

        print(f"Rolling {dice_string} -> {roll_details}: Rolls={individual_rolls}, BaseTotal={total_roll}, Modifier={modifier}, FinalResult={final_result}")

        return final_result

    def get_all_players(self) -> dict:
        """
        Returns all players in the game state.

        Returns:
            dict: A dictionary of all players.
        """
        player_dict = {}
        for player in self.players.keys():
            player_dict[player] = self.players[player].to_dict()
        return player_dict
    
    def get_all_npcs(self) -> dict:
        """
        Returns all npcs in the game state.

        Returns:
            dict: A dictionary of all npcs.
        """
        npc_dict = {}
        for npc in self.npcs.keys():
            npc_dict[npc] = self.npcs[npc].to_dict()
        return npc_dict
    
    def get_all_locations(self) -> dict:
        """
        Returns all locations in the game state.

        Returns:
            dict: A dictionary of all locations.
        """
        location_dict = {}
        for location in self.locations.keys():
            location_dict[location] = self.locations[location].to_dict()
        return location_dict

    def get_history(self) -> list:
        """
        Returns the game history.

        Returns:
            list: A list of actions in the game history.
        """
        return self.history
    
    def print_state(self) -> None:
        """
        Prints the current state of the game.
        """
        print("Current Game State:")
        print("Players:")
        for player in self.players.keys():
            print(player)
            print(self.players[player].to_dict())
        print("Locations:")
        for location in self.locations.keys():
            print(location)
            print(self.locations[location].to_dict())
        print("NPCs:")
        for npc in self.npcs.keys():
            print(npc)
            print(self.npcs[npc].to_dict())
        for history in self.history:
            print("**********************************************")
            print(history)