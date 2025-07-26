"""
Review Data Model
Member 2: Data Models
"""

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
        self.timestamp = datetime.now().isoforma