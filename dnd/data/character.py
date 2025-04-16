from abc import ABC, abstractmethod
from .item import Item

class Character(ABC):
    def __init__(self, name: str):
        """
        Initialize a character with a name, hp, attack, defense, level, and inventory.
        """
        self.name = name
        self.description = ""
        self.hp = 10
        self.attack = 1
        self.defense = 1
        self.level = 0
        self.money = 10
        self.inventory = []
        self.max_weight_to_carry = 10
        self.location = None
        
    
    def to_dict(self):
        """
        Convert the character to a dictionary representation.
        """
        return {
            'name': self.name,
            'description': self.description,
            'hp': self.hp,
            'attack': self.attack,
            'defense': self.defense,
            'level': self.level,
            'money': self.money,
            'inventory': [item.to_dict() for item in self.inventory],
            'max_weight_to_carry': self.max_weight_to_carry,
            'location': self.location
        }
    
    def from_dict(self, data):
        """
        Populate the character from a dictionary representation.
        """
        self.name = data['name']
        self.description = data['description']
        self.hp = data['hp']
        self.attack = data['attack']
        self.defense = data['defense']
        self.level = data['level']
        self.money = data['money']
        self.inventory = [Item().from_dict(item_data) for item_data in data['inventory']]
        self.max_weight_to_carry = data['max_weight_to_carry']
        self.location = data['location']
        return self # Return self to allow method chaining if needed