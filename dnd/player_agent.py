class PlayerAgent:
    def __init__(self, player_name):
        self.name = player_name

    def get_player_action(self):
        action = input(f"What do you want to do? ")
        return action