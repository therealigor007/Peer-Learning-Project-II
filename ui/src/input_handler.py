class InputHandler:
    def get_input(self, prompt):
        user_input = input(prompt)
        return user_input.strip()

    def validate_input(self, user_input, valid_options):
        if user_input not in valid_options:
            print("Invalid input. Please try again.")
            return False
        return True

    def handle_input(self, prompt, valid_options):
        while True:
            user_input = self.get_input(prompt)
            if self.validate_input(user_input, valid_options):
                return user_input