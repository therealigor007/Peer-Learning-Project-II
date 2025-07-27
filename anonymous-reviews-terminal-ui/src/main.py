# filepath: anonymous-reviews-terminal-ui/src/main.py

from menu import Menu
from display import Display
from input_handler import InputHandler

def main():
    display = Display()
    menu = Menu(display)
    input_handler = InputHandler()

    while True:
        display.clear_screen()
        menu.show()
        selection = input_handler.get_menu_selection()

        if selection == '1':
            # Logic to submit a review
            pass
        elif selection == '2':
            # Logic to view reviews
            pass
        elif selection == '3':
            # Logic to exit the program
            print("Exiting the program. Thank you!")
            break
        else:
            display.show_message("Invalid selection. Please try again.")

if __name__ == "__main__":
    main()