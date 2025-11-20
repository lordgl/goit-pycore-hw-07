from typing import Callable

from colorama import Fore

from helpers import (
    validate_name,
    validate_phone_number,
    input_error,
    display_success_message,
    validate_args_count,
    style_text,
)
from instances import AddressBook, Record


def greeting() -> str:
    return "Hello, How can I assist you today?"


@input_error
def add_contact(name: str, phone_number: str, address_book: AddressBook) -> bool:
    """Adds a new contact record or phone to the address book."""
    if not validate_name(name):
        raise ValueError("Invalid name format. Name should contain only alphabetic characters.")
    if not validate_phone_number(phone_number):
        raise ValueError(
            "Invalid phone number format. It should start with '+' followed by 7-15 digits or "
            "'0' followed by 6-14 digits."
        )

    record = address_book.find(name)
    if record is None:
        record = Record(name)
        add_message = record.add_phone(phone_number)
        if add_message != "Phone number is set":
            raise ValueError(add_message)
        address_book.add_record(record)
    else:
        if record.find_phone(phone_number):
            raise ValueError(f"Contact {name} already has this phone number.")
        add_message = record.add_phone(phone_number)
        if add_message != "Phone number is set":
            raise ValueError(add_message)
    return True


@input_error
def change_contact(name: str, new_phone_number: str, address_book: AddressBook) -> bool:
    """Changes the primary phone number of an existing contact."""
    if not validate_phone_number(new_phone_number):
        raise ValueError(
            "Invalid phone number format. It should start with '+' followed by 7-15 digits or "
            "'0' followed by 6-14 digits."
        )

    record = address_book.find(name)
    if record is None:
        raise ValueError("Contact not found.")

    if not record.phones:
        add_message = record.add_phone(new_phone_number)
        if add_message != "Phone number is set":
            raise ValueError(add_message)
        return True

    current_phone = record.phones[0].value
    update_message = record.edit_phone(current_phone, new_phone_number)
    if update_message != "Phone number is set":
        raise ValueError(update_message)
    return True


def close() -> str:
    return "Goodbye! Have a great day!"


@input_error
def handle_hello(args: list[str]) -> None:
    """ 
    Handles the 'hello' command to greet the user and display a greeting message.
    Args:
        args (list[str]): List of arguments provided with the command.
    Raises:
        ValueError: If unexpected arguments are provided.
    """
    validate_args_count(args, 0, "hello")
    print(style_text(greeting(), color=Fore.CYAN, bright=True))


@input_error
def handle_add(args: list[str], address_book: AddressBook) -> None:
    """ 
    Handles the 'add' command to add a new contact to the address book and display a success message.
    Args:
        args (list[str]): List of arguments provided with the command.
        address_book (AddressBook): The address book to add the new contact to.
    Raises:
        ValueError: If the contact already exists or if the input format is invalid.
    """
    validate_args_count(args, 2, "add [name] [phone_number]")
    name, phone_number = args
    if add_contact(name, phone_number, address_book):
        display_success_message(f"Contact {name} added with phone number {phone_number}")


@input_error
def handle_change(args: list[str], address_book: AddressBook) -> None:
    """ 
    Handles the 'change' command to update an existing contact's phone number and display a success message.
    Args:
        args (list[str]): List of arguments provided with the command.
        address_book (AddressBook): The address book storing contact records.
    Raises:
        ValueError: If the contact does not exist or if the input format is invalid.
    """
    validate_args_count(args, 2, "change [name] [new_phone_number]")
    name, new_phone_number = args
    if change_contact(name, new_phone_number, address_book):
        display_success_message(f"Contact {name} updated with new phone number {new_phone_number}")


@input_error
def handle_phone(args: list[str], address_book: AddressBook) -> None:
    """
    Handles the 'phone' command to retrieve and display a contact's phone number(s).
    Args:
        args (list[str]): List of arguments provided with the command.
        address_book (AddressBook): The address book to retrieve the contact from.
    Raises:
        ValueError: If the contact does not exist or if the input format is invalid.
    """
    validate_args_count(args, 1, "phone [name]")
    name = args[0]
    record = address_book.find(name)
    if record is None:
        raise ValueError(f"Contact {name} not found.")
    phone_numbers = "; ".join(phone.value for phone in record.phones) or "No phone numbers"
    name_part = style_text(name, color=Fore.BLUE, bright=True)
    label_part = style_text("'s phone number(s): ", color=Fore.BLUE)
    phone_part = style_text(phone_numbers, color=Fore.BLUE, bright=True)
    print(f"{name_part}{label_part}{phone_part}")


@input_error
def handle_all(args: list[str], address_book: AddressBook) -> None:
    """
    Handles the 'all' command to display all contacts in the address book.
    Args:
        args (list[str]): List of arguments provided with the command.
        address_book (AddressBook): The address book to list contacts from.
    Raises:
        ValueError: If unexpected arguments are provided.
    """
    validate_args_count(args, 0, "all")
    if not address_book:
        raise ValueError("No contacts found.")
    contacts = ["Contacts List:"]
    for name, record in address_book.items():
        phones = "; ".join(phone.value for phone in record.phones) or "No phone numbers"
        contacts.append(f"{name}: {phones}")
        
    print(style_text("\n".join(contacts), color=Fore.YELLOW))



@input_error
def handle_exit(args: list[str]) -> None:
    """
    Handles the exit commands to terminate the application and display a goodbye message.
    Args:
        args (list[str]): List of arguments provided with the command.
    Raises:
        ValueError: If unexpected arguments are provided.
    """
    validate_args_count(args, 0, "exit/close/bye/q")
    print(style_text(close(), color=Fore.MAGENTA, bright=True))
    raise SystemExit


@input_error
def handle_menu(args: list[str], menu_provider: Callable[[], str]) -> None:
    """
    Handles the 'menu' command to display the main menu options to the user.
    Args:
        args (list[str]): List of arguments provided with the command.
        menu_provider (Callable[[], str]): A callable that returns the menu string.
    Raises:
        ValueError: If unexpected arguments are provided.
    """
    validate_args_count(args, 0, "menu")
    print(menu_provider())