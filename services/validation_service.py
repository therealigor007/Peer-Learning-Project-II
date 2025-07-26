"""
Input Validation Service
Member 3: Storage & Business Logic
"""

from config.settings import Settings

class ValidationService:
    def _init_(self):
        """Initialize validation service"""
        self.settings = Settings()
    
    def validate_review(self, category_id, item_name, rating, content):
        """Validate all review input data"""
        
        # Check category ID
        if not isinstance(category_id, int) or not (1 <= category_id <= 4):
            return False, "Category must be 1, 2, 3, or 4"
        
        # Check item name
        if not item_name or len(item_name.strip()) < 2:
            return False, "Item name must be at least 2 characters"
        
        # Check rating
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            return False, "Rating must be between 1 and 5"
        
        # Check content length
        content = content.strip()
        if len(content) < self.settings.MIN_REVIEW_LENGTH:
            return False, f"Review must be at least {self.settings.MIN_REVIEW_LENGTH} characters"
        
        if len(content) > self.settings.MAX_REVIEW_LENGTH:
            return False, f"Review cannot exceed {self.settings.MAX_REVIEW_LENGTH} characters"
        
        # Check for inappropriate content
        if self._contains_inappropriate_content(content):
            return False, "Review contains inappropriate content"
        
        return True, "Valid"
    
    def _contains_inappropriate_content(self, content):
        """Check for inappropriate words"""
        content_lower = content.lower()
        for word in self.settings.INAPPROPRIATE_WORDS:
            if word in content_lower:
                return True
        return False
    
    def validate_search_term(self, search_term):
        """Validate search input"""
        if not search_term or len(search_term.strip()) < 2:
            return False, "Search term must be at least 2 characters"
        return True, "Valid"