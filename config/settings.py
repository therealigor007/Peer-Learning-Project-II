class Settings:
    # Review validation rules
    MAX_REVIEW_LENGTH = 500
    MIN_REVIEW_LENGTH = 10
    MIN_RATING = 1
    MAX_RATING = 5
    
    # Default categories for the application
    DEFAULT_CATEGORIES = [
        {"id": 1, "name": "Courses", "description": "Academic courses and modules"},
        {"id": 2, "name": "Services", "description": "Library, Dining, IT Support"},
        {"id": 3, "name": "Locations", "description": "Study Spaces, Facilities"},
        {"id": 4, "name": "Events", "description": "University events and activities"}
    ]
    
    # Basic content filtering
    INAPPROPRIATE_WORDS = ["spam", "inappropriate", "offensive"]