#!/usr/bin/env python3
import json
import random
import statistics

with open('animals.json', 'r') as f:
    animals = json.load(f)


def print_animal(index):
    print('head:', animals['animals'][index]['head'])
    print('body:', animals['animals'][index]['body'])
    print('arms:', animals['animals'][index]['arms'])
    print('legs:', animals['animals'][index]['legs'])
    print('tails:', animals['animals'][index]['tails'])


# Gets the mean of the arms, legs, and tails within the population. Rounds down.
def mean_median_mode_appendages():
    # We know the size has to be 20.
    list_arms = [0] * 20
    list_legs = [0] * 20
    list_tails = [0] * 20

    for i in range(20):
        list_arms[i] = animals['animals'][i]['arms']
        list_legs[i] = animals['animals'][i]['legs']
        list_tails[i] = animals['animals'][i]['tails']

    # Methods pulled from the statistics library.
    mean = [int(statistics.mean(list_arms)), int(statistics.mean(list_legs)), int(statistics.mean(list_tails))]
    median = [int(statistics.median(list_arms)), int(statistics.median(list_legs)), int(statistics.median(list_tails))]
    mode = [int(statistics.mode(list_arms)), int(statistics.mode(list_legs)), int(statistics.mode(list_tails))]

    return mean, median, mode


# Gets the mode of the names of the head types.
def head_count():
    # We know the size has to be 20.
    list_head = [None] * 20

    for i in range(20):
        list_head[i] = animals['animals'][i]['head']

    # Creates new array that'll only have one of each head part.
    reffHead = ["Error, multiple modes for head parts"] # Error message in case that there are multiple modes,
                                                        # you can't average out the modes if they aren't numbers.

    for i in range(20):
        currHead = list_head[i]

        # Checks within reffHead if the head already exists
        for j in range(len(reffHead)):
            if currHead == reffHead[j]:
                break
            elif j == (len(reffHead) - 1):
                reffHead.append(currHead)
                break

    # Goes through the original list and counts the heads.
    countHead = [0] * len(reffHead)

    for i in range(len(reffHead)):
        currHead = reffHead[i]

        for j in range(20):
            if currHead == list_head[j]:
                countHead[i] += 1

    return reffHead, countHead


# Same as head_count, but it'll split the body parts between the hyphen and count them. Name picked for readability.
def body_count():
    # We know the size has to be 20.
    list_body = [None] * 20

    for i in range(20):
        list_body[i] = animals['animals'][i]['body']

    # Creates new array that'll only have one of each body part.
    reffBody = ["Error, multiple modes for head parts"]
    unorganized_reffBody = [""]

    for i in range(20):
        currBody = list_body[i]
        # Seperate the body parts between the hyphen
        bodyParts = ["", ""]
        iterParts = 0

        for character in currBody:
            if character == "-":
                iterParts = 1
                continue
            bodyParts[iterParts] += character

        for i in range(1):
            unorganized_reffBody.append(bodyParts[i])

        # Add body parts to reffBody as long as it's not there already
        for j in range(1):
            for k in range(len(reffBody)):
                if bodyParts[j] == reffBody[k]:
                    break
                elif k == (len(reffBody) - 1):
                    reffBody.append(bodyParts[j])
                    break

    unorganized_reffBody.pop(0) # Removes the first index at the start, kinda an ugly workaround.

    # Goes through the original list and counts the bodies. Same code as above.
    countBody = [0] * len(reffBody)

    for i in range(len(reffBody)):
        currBody = reffBody[i]

        for j in range(len(unorganized_reffBody)):
            if currBody == unorganized_reffBody[j]:
                countBody[i] += 1

    return reffBody, countBody


# Finds the index of the mode in reff and count for the name and number. The provided mode() method spits out a hard
# error if there are multiple modes. This way, I can just print an error msg.
def mode_count(count_list):
    num = 0 # The count of the certain body or head part
    iter = 0 # The index of the part within reffHead and reffBody

    for i in range(len(count_list)):
        if num < count_list[i]:
            num = count_list[i]
            iter = i

        # In the case of multiple modes, return error message.
        elif num == count_list[i]:
            iter = 0

    return iter


## Main function
def main():
    rand_num = random.randrange(0, 19, 1)
    print_animal(rand_num)
    print("\n")

    mean, median, mode = mean_median_mode_appendages()
    reffHead, countHead = head_count()
    reffBody, countBody = body_count()

    iterHead = mode_count(countHead) # for reff and count variables.
    iterBody = mode_count(countBody)

    print("Mean:")
    print(" Arms: ", mean[0])
    print(" Legs: ", mean[1])
    print(" Tails: ", mean[2])
    print("")
    print("Median:")
    print(" Arms: ", median[0])
    print(" Legs: ", median[1])
    print(" Tails: ", median[2])
    print("")
    print("Mode:")
    print(" Arms: ", mode[0])
    print(" Legs: ", mode[1])
    print(" Tails: ", mode[2])
    print("\n")

    print("Most common head part: ", reffHead[iterHead])
    print("Most common half-body part: ", reffBody[iterBody])


if __name__ == '__main__':
    main()

