import colorama
from colorama import Fore
from functools import partial

from helpers import parse_input, display_error_message, style_text
from handlers import (
    handle_hello,
    handle_add,
    handle_change,
    handle_phone,
    handle_all,
    handle_exit,
    handle_menu,
)
from instances import AddressBook

ADDRESS_BOOK = AddressBook()  # In-memory contacts database

EXIT_COMMANDS = {'exit', 'close', 'bye', 'q'}


def main_menu() -> str:
    """
    Displays the main menu options to the user.
    Returns:
        str: The main menu string.
    """
    title = style_text("Please choose an option:", color=Fore.BLUE, bright=True)

    def option(command: str) -> str:
        return style_text(command, color=Fore.CYAN)

    menu_text = (
        f"{title}\n"
        f"  {option('* hello')} - Greet the user\n"
        f"  {option('* add [name] [phone_number]')} - Add a new contact (+7-15 digits or 0 +6-14 digits)\n"
        f"  {option('* change [name] [new_phone_number]')} - Update an existing contact's primary phone\n"
        f"  {option('* phone [name]')} - Retrieve a contact's phone number(s)\n"
        f"  {option('* all')} - Display all contacts\n"
        f"  {option('* exit/close/bye/q')} - Exit the application\n"
        f"  {option('* menu')} - Show this menu again"
    )
    return menu_text

"""
Command to handler mapping
"""
COMMAND_HANDLERS = {
    'hello': handle_hello,
    'add': partial(handle_add, address_book=ADDRESS_BOOK),
    'change': partial(handle_change, address_book=ADDRESS_BOOK),
    'phone': partial(handle_phone, address_book=ADDRESS_BOOK),
    'all': partial(handle_all, address_book=ADDRESS_BOOK),
    'menu': partial(handle_menu, menu_provider=main_menu),
}


def _handle_command(command: str, args: list[str]) -> None:
    """
    Handles commands based on user input.
    Args:
        command (str): The command to handle.
        args (list[str]): List of arguments provided with the command.
    Raises:
        SystemExit: If the exit command is invoked.
    """
    if not command:
        return

    if command in EXIT_COMMANDS:
        handle_exit(args)
        return

    handler = COMMAND_HANDLERS.get(command)
    if handler:
        handler(args)
    else:
        display_error_message("Unknown command. Type 'menu' to see available options.")


def main():
    """
    Main function to run the command-line bot application.
    """
    colorama.init(autoreset=True)
    print(main_menu())
    while True:
        user_input = input(style_text("Enter command: ", color=Fore.BLUE))
        command, args = parse_input(user_input)
        print()
        _handle_command(command, args)
        print()


if __name__ == "__main__":
    main()