from datetime import datetime
import uuid

class Review:
    def __init__(self, category_id, item_name, rating, content):
        """Create a new review"""
        self.id = str(uuid.uuid4())
        self.category_id = category_id
        self.item_name = item_name.strip()
        self.rating = rating
        self.content = content.strip()
        self.anonymous_id = f"user_{str(uuid.uuid4())[:8]}"
        self.timestamp = datetime.now().isoformat()
        self.helpful_votes = 0
        self.flagged = False  # Add flagged field for compatibility
    
    def to_dict(self):
        """Convert review to dictionary for storage"""
        return {
            "id": self.id,
            "category_id": self.category_id,
            "item_name": self.item_name,
            "rating": self.rating,
            "content": self.content,
            "anonymous_id": self.anonymous_id,
            "timestamp": self.timestamp,
            "helpful_votes": self.helpful_votes,
            "flagged": self.flagged
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create review from dictionary (when loading from database)"""
        review = cls.__new__(cls)  # Create instance without calling __init__
        review.id = data["id"]
        review.category_id = data["category_id"]
        review.item_name = data["item_name"]
        review.rating = data["rating"]
        review.content = data["content"]
        review.anonymous_id = data["anonymous_id"]
        review.timestamp = data["timestamp"]
        review.helpful_votes = data.get("helpful_votes", 0)
        review.flagged = data.get("flagged", False)
        return review
    
    def __str__(self):
        """String representation for debugging"""
        return f"Review for {self.item_name}: {self.rating}/5 stars"