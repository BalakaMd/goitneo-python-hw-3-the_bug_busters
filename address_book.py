from collections import UserDict
from datetime import date
import re


def data_validator(func):
    """
    Wrapper function.
    Validates a phone number and birthday date in special format.
    :param func:
    :return wrapper:
    """

    def inner(*args, **kwargs):
        """
        Handles exception 'ValueError' if the phone number or birthday is in incorrect format.
        :param args:
        :param kwargs:
        :return None:
        """
        try:
            func(*args, **kwargs)
        except ValueError:
            if func.__name__ == 'add_birthday':
                print("Birthday date must in this format 'DD.MM.YYYY'\n")
            else:
                print("Phone number must be 10 digits long\n")

    return inner


class Field:
    """
    Base class for record fields.
    """

    def __init__(self, value: str):
        """
        Initializes a Field object with a given value.
        :param value:
        """
        self.value = value

    def __str__(self):
        """
        Returns the string representation of the field value.
        :return str(self.value):
        """
        return str(self.value)


class Name(Field):
    """
    Class to store contact names. Mandatory field.
    """

    def __init__(self, value: str):
        super().__init__(value)
        self.name = value


class Phone(Field):
    """
    Class to store phone numbers. Validates the phone number using
    validate_phone_number function for thr required format (10 digits).
    """

    def __init__(self, value: str):
        """
        Initializes a Phone object with a given value.
        :param value:
        """
        super().__init__(value)
        self.phone = self.validate_phone_number()

    def validate_phone_number(self):
        """
        Validates the required format (10 digits) of the phone number.
        :return: Raises 'ValueError' if the phone number format is invalid.
        """
        if re.findall(r'^\d{10}$', str(self.value.replace('+38', ''))):
            print("Contacts updated.\n")
            return self.value
        else:
            raise ValueError("Phone number must be 10 digits long.")


class Birthday(Field):
    def __init__(self, value: str):
        super().__init__(value)
        self.birthday = self.validate_birthday()

    def validate_birthday(self):
        date_pattern = re.compile(r'^\d{2}\.\d{2}\.\d{4}$')
        """
        Validates the required format (DD.MM.YYYY) of the birthday date.
        :return: Raises 'ValueError' if the birthday date format is invalid.
        """
        if date_pattern.match(self.value):
            day, month, year = self.value.split('.')
            if int(day) <= 31 and int(month) <= 12:
                print("Birthday added.\n")
                return date(int(year), int(month), int(day))
            print("Birthday date must in this format 'DD.MM.YYYY'\n")
        else:
            raise ValueError("Birthday date must in this format 'DD.MM.YYYY'")


class Record:
    """
    Class to store contact information including name and phone numbers.
    """

    def __init__(self, name: str):
        """
        Initializes a Record object with a given name.
        :param name:
        """
        self.name = Name(name.lower())
        self.phones = []
        self.birthday = 'Unknown'

    @data_validator
    def add_phone(self, phone: str):
        """
        Adds a phone number to the contact.
        :param phone:
        :return None:
        """
        self.phones.append(Phone(phone))

    def remove_phone(self, phone_number: str):
        """
        Removes a phone number from the contact.
        :param phone_number:
        :return None:
        """
        for p in self.phones:
            if p.value == phone_number:
                self.phones.remove(p)

    @data_validator
    def edit_phone(self, old_phone_number: str, new_phone_number: str):
        """
        Edits a phone number in the phone list.
        :param old_phone_number:
        :param new_phone_number:
        :return None:
        """
        for p in self.phones:
            if p.value == old_phone_number:
                p.value = str(Phone(str(new_phone_number)))

    def find_phone(self, phone_number: str):
        """
        Searches for a specific phone number in the contact.
        :param phone_number:
        :return phone_number if found, None otherwise:
        """
        for p in self.phones:
            if p.value == phone_number:
                return phone_number

    @data_validator
    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def __str__(self):
        """
        Returns the string representation of the contact information.
        :return contact string representation:
        """
        return f"Contact name: {self.name.value.title()}, phones: {'; '.join(p.value for p in self.phones)}," \
               f" birthday: {self.birthday} "


class AddressBook(UserDict):
    """
    Class to manage and store records in an address book.
    """

    def add_record(self, user: Record):
        """
        Adds a record to the address book.
        :param user:
        :return None:
        """
        self.data[user.name.value] = user

    def find(self, name: str):
        """
        Finds a record in the address book by name.
        :param name:
        :return returns the string representation of the contact information:
        """
        return f'{self.data.get(name.lower())}\n'

    def delete(self, name: str):
        """
        Deletes a record from the address book by name.
        :param name:
        :return None:
        """
        if name.lower() in self.data:
            del self.data[name.lower()]
