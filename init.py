from dotenv import load_dotenv
import os


load_dotenv()
def get_enviroment_variable(key: str) -> str:
    data: str = os.environ.get(key)
    if not data:
        raise KeyError(f"Key {key} not found")

    return data