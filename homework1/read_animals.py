import json
import random

with open('animals.json', 'r') as f:
    animals = json.load(f)


def print_animal(index):
    print('head:', animals['animals'][index]['head'])
    print('body:', animals['animals'][index]['body'])
    print('arms:', animals['animals'][index]['arms'])
    print('legs:', animals['animals'][index]['legs'])
    print('tails:', animals['animals'][index]['tails'])


rand_num = random.randrange(0, 19, 1)
print_animal(rand_num)