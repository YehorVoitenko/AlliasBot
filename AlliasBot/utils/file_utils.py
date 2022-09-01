import json
import random

from Allias.constants.paths import NOUNS, ADJECTIVES, WORDS, EN_TRANSLATIONS
from Allias.models.translation import Translation


def get_random_name():
    with open(NOUNS, 'r') as file:
        data = file.read()
        nouns = data.split("\n")
        noun = random.choice(nouns)

    with open(ADJECTIVES, 'r') as file:
        data = file.read()
        adjectives = data.split("\n")
        adjective = random.choice(adjectives)

    name = noun.capitalize() + adjective.capitalize()
    return name


def get_random_word():
    with open(WORDS, 'r') as file:
        data = file.read()
        words = data.split("\n")
        word = random.choice(words)

    return word.capitalize()


def get_translation(file: str = EN_TRANSLATIONS):
    with open(file) as text:
        kwargs = json.load(text)
    return Translation(**kwargs)
