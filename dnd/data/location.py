from .item import Item
from .npc import Npc
LOCATION_EXAMPLE = """{
    "name": "Forest",
    "description": "A dense forest filled with tall trees and wildlife.",
    "items": [
        {
            "name": "Sword",
            "description": "A sharp blade.",
            "weight": 5.0,
            "value": 100.0,
            "health": 10
        }
    ],
    "npcs": [
        {
            "name": "Goblin",
            "description": "A small green creature.",
            "hp": 5,
            "attack": 2,
            "defense": 1,
            "level": 1,
            "inventory": [],
            "max_weight_to_carry": 10,
            "location": null
        }
    ],
    "neighbours": ["Cave", "Mountain"],
    "visited": false
}
"""
class Location():
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.items = []
        self.npcs = []
        self.neighbours = []
        self.visited = False

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'items': [item.to_dict() for item in self.items],
            'npcs': [npc.to_dict() for npc in self.npcs],
            'neighbours': self.neighbours,
            'visited': self.visited
        }
    
    def from_dict(self, data):
        """
        Populate the character from a dictionary representation.
        """
        self.name = data['name']
        self.description = data['description']
        self.items = [Item().from_dict(item_data) for item_data in data['items']]
        self.npcs = [Npc('').from_dict(npc_data) for npc_data in data['npcs']]
        self.neighbours = data['neighbours']
        self.visited = data['visited']
    