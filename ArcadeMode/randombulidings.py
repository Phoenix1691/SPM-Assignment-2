import random

BUILDING_TYPES = ["R", "I", "C", "O", "*"]

def generate_two_random_buildings():
    return random.sample(BUILDING_TYPES, 2)
