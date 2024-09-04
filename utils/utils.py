import aiohttp
from faker import Faker
from constants import GPT_TOKEN



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


async def create_assistance(instruction: str, name: str):

    assistance_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GPT_TOKEN}",
        "OpenAI-Beta": "assistants=v2"
    }

    create_assistance_data = {
        "instructions": instruction,
        "name": name,
        "tools": [{"type": "code_interpreter"}],
        "model": "gpt-4o-mini"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post("https://api.openai.com/v1/assistants",
                                headers=assistance_headers,
                                json=create_assistance_data) as response:
            return await response.json()

