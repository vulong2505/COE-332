import random
import petname
import json

# msg = help(petname)
# print(msg)

head = ['snake', 'bull', 'lion', 'raven', 'bunny']

data = {}
data['animals'] = []

for i in range(20):

    random_head = random.choice(head)
    random_body = petname.name(8) + '-' + petname.name(8)
    random_arm = random.randrange(2, 10, 2)
    random_leg = random.randrange(3, 12, 3)
    num_tail = random_arm + random_leg

    data['animals'].append( {'head' : random_head, 'body' : random_body, 'arms' : random_arm,
                             'legs' : random_leg, 'tails' : num_tail} )

with open('animals.json', 'w') as out:
    json.dump(data, out, indent=2)