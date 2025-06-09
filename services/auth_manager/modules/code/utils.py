import random
import string

def generate_code_string(length: int = 8) -> str:
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))