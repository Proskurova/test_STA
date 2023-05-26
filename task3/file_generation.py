import time
import string
import secrets


def file_generation():

    alphabet = string.ascii_letters + string.digits
    count_sec = 0

    while count_sec < 120:
        name = ''.join(secrets.choice(alphabet) for i in range(6))
        with open(f'data/{name}.txt', 'w+') as f:
            f.write(name)
        time.sleep(5)
        count_sec += 5


file_generation()