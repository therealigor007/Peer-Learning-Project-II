class Menu:
    def __init__(self):
        self.options = {
            '1': 'Submit a Review',
            '2': 'View All Reviews',
            '3': 'Search Reviews',
            '4': 'View Categories',
            '5': 'Exit'
        }

    def show_menu(self):
        print("\n--- Anonymous Reviews Menu ---")
        for key, value in self.options.items():
            print(f"{key}. {value}")

    def get_user_selection(self):
        selection = input("Please select an option: ")
        return selection.strip()

    def handle_selection(self, selection):
        if selection in self.options:
            return self.options[selection]
        else:
            print("Invalid selection. Please try again.")
            return None