class Display:
    def show_reviews(self, reviews):
        """Display a list of reviews to the user."""
        if not reviews:
            print("No reviews available.")
            return
        
        print("Reviews:")
        for review in reviews:
            print(f"Item: {review.item_name}, Rating: {review.rating}, Content: {review.content}")
            print("-" * 40)

    def show_categories(self, categories):
        """Display a list of categories to the user."""
        if not categories:
            print("No categories available.")
            return
        
        print("Categories:")
        for category in categories:
            print(f"ID: {category.id}, Name: {category.name}, Description: {category.description}")
            print("-" * 40)

    def show_message(self, message):
        """Display a message to the user."""
        print(message)