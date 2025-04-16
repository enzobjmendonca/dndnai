from .character import Character

NPC_EXAMPLE = """{
    "name": "Goblin",
    "description": "A small green creature.",
    "hp": 5,
    "attack": 2,
    "defense": 1,
    "level": 1,
    "money": 0,
    "inventory": [],
    "max_weight_to_carry": 10,
    "location": null,
    "dialogue": ["Hello there, traveler!", "Watch your step, it's dangerous here."],
    "mood": "neutral"
}
"""
class Npc(Character):
    def __init__(self, name):
        super().__init__(name)
        self.dialogue = []
        self.mood = 'neutral'

    def to_dict(self):
        character_features = super().to_dict()
        npc_features = {
            'dialogue': self.dialogue, 
            'mood': self.mood
        }
        return character_features | npc_features
    
    def from_dict(self, data):
        super().from_dict(data)
        self.dialogue = data['dialogue']
        self.mood = data['mood']
        return self