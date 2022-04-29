from functools import lru_cache
import json


@lru_cache
def read(path):
    with open(path, encoding='utf-8') as file:
        return json.load(file)


def write(path, data):
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
