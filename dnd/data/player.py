from .character import Character

PLAYER_EXAMPLE = """{
    "name": "Lucius",
    "description": "Lucius is a brave warrior from the North Rift, he is known for his habit of making good friends while drinking.",
    "hp": 10,
    "attack": 5,
    "defense": 2,
    "level": 1,
    "money": 10,
    "inventory": [{
        "name": "Sword",
        "description": "A sharp blade.",
        "weight": 5.0,
        "value": 100.0,
        "health": 10
    }],
    "max_weight_to_carry": 10,
    "location": null,
    "race": "Human",
    "class_type": "Warrior"
}
"""
class Player(Character):
    def __init__(self, name: str, race: str = 'Human', class_type: str = 'Peasant'):
        """
        Initialize a player with a name, health, attack, defense, level, and inventory.
        """
        super().__init__(name)
        self.description = "Player"
        self.race = race
        self.class_type = class_type
    
    def to_dict(self):
        character_features = super().to_dict()
        player_features = {
            'race': self.race,
            'class_type': self.class_type
        }
        return character_features | player_features
    
    def from_dict(self, data):
        super().from_dict(data)
        self.location = data['location']
        self.race = data['race']
        self.class_type = data['class_type']
        return self