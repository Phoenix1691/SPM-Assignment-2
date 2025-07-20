# randombulidings.py - Module to generate random building types for the game
import random

BUILDING_TYPES = ["R", "I", "C", "O", "*"]

def generate_two_random_buildings():
    return random.sample(BUILDING_TYPES, 2)
