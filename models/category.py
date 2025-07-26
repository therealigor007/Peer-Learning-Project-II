"""
Category Data Model
Member 2: Data Models
"""

class Category:
    def _init_(self, id, name, description=""):
        """Create a new category"""
        self.id = id
        self.name = name
        self.description = description
    
    def to_dict(self):
        """Convert category to dictionary for storage"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create category from dictionary (when loading from database)"""
        return cls(
            id=data["id"],
            name=data["name"],
            description=data.get("description", "")
        )
    
    def _str_(self):
        """String representation for debugging"""
        return f"{self.name}: {self.description}"