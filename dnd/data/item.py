"""
Item Example:
{
    "name": "Sword",
    "description": "A sharp blade.",
    "weight": 5.0,
    "value": 100.0,
    "health": 10
}
"""
class Item():

    def __str__(self):
        return f"{self.name}: {self.description} (Weight: {self.weight}, Value: {self.value}, Health: {self.health})"
    
    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'weight': self.weight,
            'value': self.value,
            'health': self.health
        }
    
    def from_dict(self, data):
        """
        Populate the item from a dictionary representation.
        """
        self.name = data['name']
        self.description = data['description']
        self.weight = data['weight']
        self.value = data['value']
        self.health = data['health']
        return self # Return self to allow method chaining if needed