from models.review import Review
from services.azure_storage_service import AzureStorageService
from services.validation_service import ValidationService

class ReviewService:
    def __init__(self): 
        """Initialize review service"""
        self.storage = AzureStorageService()
        self.validator = ValidationService()
    
    def submit_review(self, category_id, item_name, rating, content):
        """Submit a new review"""
        # Validate the review data
        is_valid, error_message = self.validator.validate_review(
            category_id, item_name, rating, content
        )
        
        if not is_valid:
            print(f"Validation error: {error_message}")
            return False
        
        # Create and save the review
        try:
            review = Review(category_id, item_name, rating, content)
            success = self.storage.save_review(review)
            
            if success:
                print("Review submitted successfully!")
            else:
                print("Failed to save review to database")
            
            return success
            
        except Exception as e:
            print(f"Error submitting review: {e}")
            return False
    
    def get_all_reviews(self):
        """Get all reviews from database"""
        try:
            return self.storage.load_all_reviews()
        except Exception as e:
            print(f"Error loading reviews: {e}")
            return []
    
    def get_reviews_by_category(self, category_id):
        """Get reviews for a specific category"""
        all_reviews = self.get_all_reviews()
        return [review for review in all_reviews if review.category_id == category_id]
    
    def search_reviews(self, search_term):
        """Search reviews by content or item name"""
        all_reviews = self.get_all_reviews()
        search_term = search_term.lower()
        
        results = []
        for review in all_reviews:
            if (search_term in review.item_name.lower() or 
                search_term in review.content.lower()):
                results.append(review)
        
        return results
    
    def get_categories(self):
        """Get all categories"""
        try:
            return self.storage.load_categories()
        except Exception as e:
            print(f"Error loading categories: {e}")
            return []
    
    def vote_helpful(self, review_id):
        """Mark a review as helpful"""
        try:
            success = self.storage.update_helpful_votes(review_id)
            if success:
                print("Vote recorded!")
            else:
                print("Failed to record vote")
            return success
        except Exception as e:
            print(f"Error recording vote: {e}")
            return False
    
    def get_reviews_by_item(self, item_name):
        """Get all reviews for a specific item"""
        all_reviews = self.get_all_reviews()
        return [review for review in all_reviews 
                if review.item_name.lower() == item_name.lower()]
    
    def search_reviews(self, search_term, category_id=None):
        """Search reviews by content or item name"""
        all_reviews = self.get_all_reviews()
        search_term = search_term.lower()
        
        results = []
        for review in all_reviews:
            if category_id and review.category_id != category_id:
                continue
            
            if (search_term in review.item_name.lower() or 
                search_term in review.content.lower()):
                results.append(review)
        
        return results
    
    def get_item_statistics(self, item_name):
        """Get statistics for a specific item"""
        reviews = self.get_reviews_by_item(item_name)
        
        if not reviews:
            return {"item_name": item_name, "total_reviews": 0}
        
        ratings = [review.rating for review in reviews]
        
        import statistics
        return {
            "item_name": item_name,
            "total_reviews": len(reviews),
            "average_rating": round(statistics.mean(ratings), 1),
            "rating_distribution": {i: ratings.count(i) for i in range(1, 6)},
            "total_helpful_votes": sum(review.helpful_votes for review in reviews)
        }
    
    def get_popular_items(self, category_id=None, limit=5):
        """Get most reviewed items with statistics"""
        all_reviews = self.get_all_reviews()
        
        if category_id:
            all_reviews = [r for r in all_reviews if r.category_id == category_id]
        
        # Count reviews per item
        from collections import defaultdict
        item_counts = defaultdict(int)
        for review in all_reviews:
            item_counts[review.item_name] += 1
        
        # Sort by review count and get statistics
        popular_items = []
        for item_name, count in sorted(item_counts.items(), 
                                     key=lambda x: x[1], reverse=True)[:limit]:
            stats = self.get_item_statistics(item_name)
            popular_items.append(stats)
        
        return popular_items