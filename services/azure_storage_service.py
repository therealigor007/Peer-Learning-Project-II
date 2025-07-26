"""
Azure SQL Database Storage Service
Member 3: Storage & Business Logic
"""

import pymssql
import os
from dotenv import load_dotenv
from models.review import Review
from models.category import Category

load_dotenv()

class AzureStorageService:
    def _init_(self):
        """Initialize Azure storage service"""
        self.server = os.getenv('AZURE_SQL_SERVER')
        self.database = os.getenv('AZURE_SQL_DATABASE')
        self.username = os.getenv('AZURE_SQL_USERNAME')
        self.password = os.getenv('AZURE_SQL_PASSWORD')
    
    def get_connection(self):
        """Get database connection"""
        try:
            return pymssql.connect(
                server=self.server,
                user=self.username,
                password=self.password,
                database=self.database,
                port=1433,
                timeout=30
            )
        except Exception as e:
            print(f"Database connection failed: {e}")
            return None
    
    def save_review(self, review):
        """Save a review to the database"""
        connection = self.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO reviews (id, category_id, item_name, rating, content, 
                                   anonymous_id, timestamp, helpful_votes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                review.id,
                review.category_id,
                review.item_name,
                review.rating,
                review.content,
                review.anonymous_id,
                review.timestamp,
                review.helpful_votes
            ))
            
            connection.commit()
            connection.close()
            return True
            
        except Exception as e:
            print(f"Failed to save review: {e}")
            connection.close()
            return False
    
    def load_all_reviews(self):
        """Load all reviews from database"""
        connection = self.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT id, category_id, item_name, rating, content, 
                       anonymous_id, timestamp, helpful_votes
                FROM reviews
                ORDER BY timestamp DESC
            """)
            
            reviews = []
            for row in cursor.fetchall():
                review_data = {
                    "id": row[0],
                    "category_id": row[1],
                    "item_name": row[2],
                    "rating": row[3],
                    "content": row[4],
                    "anonymous_id": row[5],
                    "timestamp": row[6].isoformat() if hasattr(row[6], 'isoformat') else str(row[6]),
                    "helpful_votes": row[7] or 0
                }
                reviews.append(Review.from_dict(review_data))
            
            connection.close()
            return reviews
            
        except Exception as e:
            print(f"Failed to load reviews: {e}")
            connection.close()
            return []
    
    def load_categories(self):
        """Load all categories from database"""
        connection = self.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT id, name, description FROM categories ORDER BY id")
            
            categories = []
            for row in cursor.fetchall():
                category_data = {
                    "id": row[0],
                    "name": row[1],
                    "description": row[2] or ""
                }
                categories.append(Category.from_dict(category_data))
            
            connection.close()
            return categories
            
        except Exception as e:
            print(f"Failed to load categories: {e}")
            connection.close()
            return []
    
    def update_helpful_votes(self, review_id):
        """Increment helpful votes for a review"""
        connection = self.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE reviews SET helpful_votes = helpful_votes + 1 WHERE id = %s",
                (review_id,)
            )
            
            connection.commit()
            connection.close()
            return True
            
        except Exception as e:
            print(f"Failed to update helpful votes: {e}")
            connection.close()
            return False