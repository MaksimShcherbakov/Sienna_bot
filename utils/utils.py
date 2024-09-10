import aiohttp
from faker import Faker
from constants import GPT_TOKEN
import re


def get_random_person():
    fake = Faker('ru_RU')

    user = {
        'name': fake.name(),
        'address': fake.address(),
        'email': fake.email(),
        'phone_number': fake.phone_number(),
        'birth_date': fake.date_of_birth(),
        'company': fake.company(),
        'job': fake.job()
    }
    return user

def extract_number(text):
    match = re.search(r'\b(\d+)\b', text)
    if match:
        return int(match.group(1))
    else:
        return None


def extract_after_keyword(input_string, keywords):
    if not isinstance(keywords, list):
        raise TypeError("keywords should be a list of strings")

    for keyword in keywords:
        if not isinstance(keyword, str):
            raise TypeError("Each keyword should be a string")

        input_string = input_string.replace(keyword, "").strip()

    return input_string

