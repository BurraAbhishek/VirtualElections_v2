import random
import string


def gen_id(size: int) -> str:
    id = ''.join([random.choice(
        string.ascii_uppercase
        + string.ascii_lowercase
        + string.digits
        ) for _ in range(size)])
    return id
