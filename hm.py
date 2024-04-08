from collections import defaultdict, UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)
    


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)  
        self.__value = None
        self.value = value


    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if len(value) == 10 and value.isdigit():
            self.__value = value
        else:
            raise ValueError('Invalid phone number')


class Birthday(Field):
    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")



class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        self.phones = [p for p in self.phones if str(p) != phone_number]


    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return f"Contact '{name}' deleted."
        else:
            return f"Contact '{name}' not found."

    def find_next_birthday(self, days=7):
        today = datetime.now().date()
        upcoming_birthdays = []
        for name, record in self.data.items():
            if record.birthday:
                next_birthday = datetime(today.year, record.birthday.date.month, record.birthday.date.day).date()
                if today <= next_birthday <= today + timedelta(days=days):
                    upcoming_birthdays.append((name, next_birthday))
        return upcoming_birthdays

    def get_upcoming_birthday(self, days=7):
        upcoming_birthdays = self.find_next_birthday(days)
        if upcoming_birthdays:
            return "\n".join(f"{name}: {birthday.strftime('%d.%m')}" for name, birthday in upcoming_birthdays)
        else:
            return "No upcoming birthdays in the next week."

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "KeyError"
        except ValueError:
            return "ValueError"
        except IndexError:
            return "IndexError"
    return wrapper


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    if len(args) < 2:
        return "Invalid command format. Usage: change [name] [new phone]"
    name, new_phone = args
    record = book.find(name)
    if record:
        record.add_phone(new_phone)
        return f"Phone number updated for {name}."
    else:
        return f"Contact '{name}' not found."

@input_error
def show_phones(args, book: AddressBook):
    if len(args) < 1:
        return "Invalid command format. Usage: phone [name]"
    name = args[0]
    record = book.find(name)
    if record:
        return "; ".join(str(phone) for phone in record.phones) if record.phones else f"No phone numbers for {name}."
    else:
        return f"Contact '{name}' not found."

@input_error
def show_all(book: AddressBook):
    if book.data:
        return "\n".join(str(record) for record in book.data.values())
    else:
        return "Address book is empty."

@input_error
def add_birthday(args, book):
    if len(args) < 2:
        return "Invalid command format. Usage: add-birthday [name] [DD.MM.YYYY]"
    name, birthday = args
    record = book.find(name)
    if record:
        try:
            record.add_birthday(birthday)
            return f"Birthday added for {name}."
        except ValueError as e:
            return str(e)
    else:
        return f"Contact '{name}' not found."

@input_error
def show_birthday(args, book):
    if len(args) < 1:
        return "Invalid command format. Usage: show-birthday [name]"
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday: {record.birthday}"
    elif record:
        return f"{name} has no birthday set."
    else:
        return f"Contact '{name}' not found."

@input_error
def birthdays(args, book):
    return book.get_upcoming_birthday()


def parse_input(user_input):
    return user_input.split()


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phones(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()