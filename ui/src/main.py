
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from menu import Menu
from display import Display
from input_handler import InputHandler
from services.review_service import ReviewService

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

class AnonymousReviewsApp:
    def __init__(self):
        self.display = Display()
        self.menu = Menu()
        self.input_handler = InputHandler()
        self.review_service = ReviewService()
        self.running = True
    
    def run(self):
        """Main application loop - exactly like your existing app"""
        print("=" * 60)
        print("    ANONYMOUS REVIEWS PLATFORM")
        print("    Your voice matters - Share honest feedback anonymously!")
        print("=" * 60)
        print()
        
        # Test database connection
        try:
            categories = self.review_service.get_categories()
            print("✓ Database connection established successfully!")
            print()
        except Exception as e:
            print(f"✗ Failed to connect to database: {e}")
            print("Please check your database configuration and try again.")
            return
        
        while self.running:
            self.show_main_menu()
            choice = self.get_menu_choice(1, 5)
            
            if choice == 1:
                self.submit_review_flow()
            elif choice == 2:
                self.browse_reviews_flow()
            elif choice == 3:
                self.search_reviews_flow()
            elif choice == 4:
                self.view_popular_items_flow()
            elif choice == 5:
                self.exit_application()
    
    def show_main_menu(self):
        """Display main menu exactly like your existing app"""
        clear_screen()
        print("\n" + "=" * 50)
        print("MAIN MENU")
        print("=" * 50)
        print("1. Submit a New Review")
        print("2. Browse Reviews")
        print("3. Search Reviews")
        print("4. View Popular Items")
        print("5. Exit Application")
        print("=" * 50)
    
    def get_menu_choice(self, min_option: int, max_option: int) -> int:
        """Get and validate menu choice"""
        while True:
            try:
                choice = input(f"\nPlease select an option ({min_option}-{max_option}): ").strip()
                choice_int = int(choice)
                
                if min_option <= choice_int <= max_option:
                    return choice_int
                else:
                    print(f"Please enter a number between {min_option} and {max_option}.")
            except ValueError:
                print("Please enter a valid number.")
    
    def submit_review_flow(self):
        """Handle review submission workflow - exactly like your existing app"""
        clear_screen()
        print("\n" + "=" * 50)
        print("SUBMIT NEW REVIEW")
        print("=" * 50)
        
        # Step 1: Select category
        categories = self.review_service.get_categories()
        if not categories:
            print("No categories available. Please contact administrator.")
            self.wait_for_enter()
            return
        
        print("\nSelect a category:")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category.name}")
            if category.description:
                print(f"   {category.description}")
        
        category_choice = self.get_menu_choice(1, len(categories))
        category_id = categories[category_choice - 1].id
        
        # Step 2: Enter item name
        item_name = self.get_item_name()
        
        # Step 3: Get rating
        rating = self.get_rating()
        
        # Step 4: Get review content
        content = self.get_review_content()
        
        # Submit review
        if self.review_service.submit_review(category_id, item_name, rating, content):
            print("\n✓ Thank you! Your review has been submitted successfully.")
        else:
            print("\n✗ Failed to submit review. Please try again.")
        
        self.wait_for_enter()
    
    def browse_reviews_flow(self):
        """Handle browse reviews workflow"""
        clear_screen()
        print("\n" + "=" * 50)
        print("BROWSE REVIEWS")
        print("=" * 50)
        
        categories = self.review_service.get_categories()
        print("\nSelect a category:")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category.name}")
            if category.description:
                print(f"   {category.description}")
        
        category_choice = self.get_menu_choice(1, len(categories))
        category_id = categories[category_choice - 1].id
        
        reviews = self.review_service.get_reviews_by_category(category_id)
        
        if not reviews:
            print(f"\nNo reviews found for {categories[category_choice - 1].name}")
        else:
            self.show_reviews_summary(reviews)
            
            # Option to view detailed reviews
            print("\nEnter item name to view detailed reviews (or press Enter to go back):")
            item_name = input().strip()
            
            if item_name:
                item_reviews = self.review_service.get_reviews_by_item(item_name)
                if item_reviews:
                    self.show_detailed_reviews(item_reviews)
                    self.review_interaction_menu(item_reviews)
                else:
                    print("No reviews found for that item.")
        
        self.wait_for_enter()
    
    def search_reviews_flow(self):
        """Handle search reviews workflow"""
        clear_screen()
        print("\n" + "=" * 50)
        print("SEARCH REVIEWS")
        print("=" * 50)
        
        search_term = self.get_search_term()
        
        # Optional category filter
        print("\nFilter by category? (y/n):")
        if input().lower().startswith('y'):
            categories = self.review_service.get_categories()
            print("\nSelect a category:")
            for i, category in enumerate(categories, 1):
                print(f"{i}. {category.name}")
                if category.description:
                    print(f"   {category.description}")
            category_choice = self.get_menu_choice(1, len(categories))
            category_id = categories[category_choice - 1].id
        else:
            category_id = None
        
        results = self.review_service.search_reviews(search_term, category_id)
        
        if not results:
            print(f"\nNo reviews found matching '{search_term}'")
        else:
            print(f"\nFound {len(results)} reviews matching '{search_term}':")
            self.show_search_results(results)
        
        self.wait_for_enter()
    
    def view_popular_items_flow(self):
        """Handle popular items display"""
        clear_screen()
        print("\n" + "=" * 50)
        print("POPULAR ITEMS")
        print("=" * 50)
        
        print("1. All categories")
        print("2. Specific category")
        
        choice = self.get_menu_choice(1, 2)
        
        if choice == 2:
            categories = self.review_service.get_categories()
            print("\nSelect a category:")
            for i, category in enumerate(categories, 1):
                print(f"{i}. {category.name}")
                if category.description:
                    print(f"   {category.description}")
            category_choice = self.get_menu_choice(1, len(categories))
            category_id = categories[category_choice - 1].id
        else:
            category_id = None
        
        popular_items = self.review_service.get_popular_items(category_id, limit=10)
        
        if not popular_items:
            print("\nNo items found.")
        else:
            self.show_popular_items(popular_items)
        
        self.wait_for_enter()
    
    def review_interaction_menu(self, reviews):
        """Handle review interaction (helpful votes)"""
        while True:
            print("\nReview Actions:")
            print("1. Mark a review as helpful")
            print("2. Back to main menu")
            
            choice = self.get_menu_choice(1, 2)
            
            if choice == 1:
                print("Enter review number to mark as helpful:")
                try:
                    review_num = int(input()) - 1
                    if 0 <= review_num < len(reviews):
                        self.review_service.vote_helpful(reviews[review_num].id)
                        print("Thank you! Your vote has been recorded.")
                    else:
                        print("Invalid review number.")
                except ValueError:
                    print("Please enter a valid number.")
            else:
                break
    
    def get_item_name(self) -> str:
        """Get and validate item name"""
        while True:
            item_name = input("\nEnter the name of the course/service/location: ").strip()
            
            if len(item_name) >= 2:
                return item_name
            else:
                print("Item name must be at least 2 characters long.")
    
    def get_rating(self) -> int:
        """Get and validate rating"""
        while True:
            try:
                print("\nRate your experience:")
                print("1 - Poor")
                print("2 - Fair") 
                print("3 - Good")
                print("4 - Very Good")
                print("5 - Excellent")
                
                rating = int(input("Your rating (1-5): ").strip())
                
                if 1 <= rating <= 5:
                    return rating
                else:
                    print("Please enter a rating between 1 and 5.")
            except ValueError:
                print("Please enter a valid number.")
    
    def get_review_content(self) -> str:
        """Get and validate review content"""
        print("\nWrite your detailed review:")
        print("(Press Enter on an empty line to finish)")
        
        lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            lines.append(line)
        
        content = " ".join(lines).strip()
        
        if len(content) < 10:
            print("Review must be at least 10 characters long. Please try again.")
            return self.get_review_content()
        
        if len(content) > 500:
            print("Review cannot exceed 500 characters. Please try again.")
            return self.get_review_content()
        
        return content
    
    def get_search_term(self) -> str:
        """Get search term from user"""
        while True:
            search_term = input("\nEnter search term (course name, keyword, etc.): ").strip()
            
            if len(search_term) >= 2:
                return search_term
            else:
                print("Search term must be at least 2 characters long.")
    
    def wait_for_enter(self):
        """Wait for user to press Enter"""
        input("\nPress Enter to continue...")
    
    def show_reviews_summary(self, reviews):
        """Display summary of reviews grouped by item - exactly like your existing app"""
        items = {}
        for review in reviews:
            if review.item_name not in items:
                items[review.item_name] = {
                    'reviews': [],
                    'total_rating': 0,
                    'count': 0
                }
            items[review.item_name]['reviews'].append(review)
            items[review.item_name]['total_rating'] += review.rating
            items[review.item_name]['count'] += 1
        
        print(f"\nFound {len(reviews)} reviews for {len(items)} items:")
        print("-" * 60)
        
        for item_name, data in items.items():
            avg_rating = data['total_rating'] / data['count']
            stars = self.format_rating(avg_rating)
            print(f"{item_name}")
            print(f"  Average Rating: {stars} ({avg_rating:.1f}/5)")
            print(f"  Total Reviews: {data['count']}")
            
            # Show latest review snippet
            latest_review = max(data['reviews'], key=lambda r: r.timestamp)
            snippet = latest_review.content[:60] + "..." if len(latest_review.content) > 60 else latest_review.content
            print(f"  Latest: \"{snippet}\"")
            print("-" * 60)
    
    def show_detailed_reviews(self, reviews):
        """Display detailed individual reviews"""
        print(f"\nDetailed Reviews ({len(reviews)} total):")
        print("=" * 60)
        
        for i, review in enumerate(reviews, 1):
            print(f"Review #{i}")
            print(f"Item: {review.item_name}")
            print(f"Rating: {self.format_rating(review.rating)} ({review.rating}/5)")
            print(f"Date: {self.format_date(review.timestamp)}")
            print(f"Review: {review.content}")
            print(f"Helpful votes: {review.helpful_votes}")
            print(f"Reviewer: {review.anonymous_id}")
            print("-" * 60)
    
    def show_search_results(self, reviews):
        """Display search results"""
        for i, review in enumerate(reviews, 1):
            print(f"\n{i}. {review.item_name} - {self.format_rating(review.rating)}")
            snippet = review.content[:100] + "..." if len(review.content) > 100 else review.content
            print(f"   \"{snippet}\"")
            print(f"   {self.format_date(review.timestamp)} | Helpful: {review.helpful_votes}")
    
    def show_popular_items(self, items):
        """Display popular items statistics"""
        print("\nMost Reviewed Items:")
        print("=" * 60)
        
        for i, item in enumerate(items, 1):
            print(f"{i}. {item['item_name']}")
            print(f"   Average Rating: {self.format_rating(item['average_rating'])} ({item['average_rating']}/5)")
            print(f"   Total Reviews: {item['total_reviews']}")
            print(f"   Total Helpful Votes: {item['total_helpful_votes']}")
            
            # Show rating distribution
            distribution = item['rating_distribution']
            print("   Rating Distribution:")
            for rating in range(5, 0, -1):
                count = distribution.get(rating, 0)
                bar = "█" * (count * 20 // max(1, item['total_reviews'])) if count > 0 else ""
                print(f"     {rating} stars: {count:2d} {bar}")
            print("-" * 60)
    
    def format_rating(self, rating: float) -> str:
        """Format rating as stars"""
        full_stars = int(rating)
        half_star = 1 if rating - full_stars >= 0.5 else 0
        empty_stars = 5 - full_stars - half_star
        
        return "★" * full_stars + "☆" * half_star + "☆" * empty_stars
    
    def format_date(self, timestamp: str) -> str:
        """Format timestamp for display"""
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(timestamp)
            return dt.strftime("%B %d, %Y")
        except:
            return timestamp
    
    def exit_application(self):
        """Handle application exit"""
        clear_screen()
        print("\nThank you for using Anonymous Reviews Platform!")
        print("Your feedback helps improve our community.")
        self.running = False

def main():
    """Main application entry point"""
    app = AnonymousReviewsApp()
    app.run()

if __name__ == "__main__":
    main()