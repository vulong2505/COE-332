import json
import statistics
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    return "Hello World!\n"


@app.route('/animals', methods=['GET'])
def get_animals():
    return json.dumps(get_data())


def get_data():
    with open("/app/data_file.json", "r") as json_file:  # for hw3, the full path is in /app/ within the docker container
        userdata = json.load(json_file)
    return userdata


@app.route('/animals/head/<head_type>', methods=['GET'])
def get_head(head_type):
    test = get_data()
    # print(type(test))

    jsonList = test['animals']
    # print(type(jsonList))

    output = [x for x in jsonList if x['head'] == head_type]
    # print(type(legs_num))

    return json.dumps(output)


@app.route('/animals/legs/<num>', methods=['GET'])
def get_legs(num):
    legs_num = int(num)  # Converts str to int

    test = get_data()
    # print(type(test))

    jsonList = test['animals']
    # print(type(jsonList))

    output = [x for x in jsonList if x['legs'] == legs_num]
    # print(type(legs_num))

    return json.dumps(output)


# curl "localhost:5035/animals/stats/arms"
@app.route('/animals/stats/<part>', methods=['GET'])
def get_stats(part):
    msg = "Error, that part doesn't exist \n"

    mean, median, mode = mean_median_mode_appendages()  # Index 0 is arms, 1 is legs, 2 is tails
    reffHead, countHead = head_count()
    reffBody, countBody = body_count()

    iterHead = mode_count(countHead)  # for reff and count variables.
    iterBody = mode_count(countBody)

    if part == "arms":
        mean_part = str(mean[0])
        median_part = str(median[0])
        mode_part = str(mode[0])

        msg = print_appendages(mean_part, median_part, mode_part)

    elif part == "legs":
        mean_part = str(mean[1])
        median_part = str(median[1])
        mode_part = str(mode[1])

        msg = print_appendages(mean_part, median_part, mode_part)

    elif part == "tails":
        mean_part = str(mean[2])
        median_part = str(median[2])
        mode_part = str(mode[2])

        msg = print_appendages(mean_part, median_part, mode_part)

    elif part == "head":
        msg = print_head(reffHead[iterHead])

    elif part == "body":
        msg = print_body(reffBody[iterBody])

    return msg


def print_appendages(mean_part, median_part, mode_part):
    msg = ("Mean: " + mean_part + "\n"
                                  "Median: " + median_part + "\n"
                                                             "Mode: " + mode_part + "\n")
    return msg


def print_head(val):
    msg = ("Most common head part: " + val + "\n")
    return msg


def print_body(val):
    msg = ("Most common half-body part: " + val + "\n")
    return msg


# Gets the mean of the arms, legs, and tails within the population. Rounds down.
def mean_median_mode_appendages():
    # Gets the json data
    animals = get_data()

    # We know the size has to be 100.
    list_arms = [0] * 100
    list_legs = [0] * 100
    list_tails = [0] * 100

    for i in range(100):
        list_arms[i] = animals['animals'][i]['arms']
        list_legs[i] = animals['animals'][i]['legs']
        list_tails[i] = animals['animals'][i]['tails']

    # Methods pulled from the statistics library. Data from left to right: arms, legs, and tails.
    mean = [int(statistics.mean(list_arms)), int(statistics.mean(list_legs)), int(statistics.mean(list_tails))]
    median = [int(statistics.median(list_arms)), int(statistics.median(list_legs)), int(statistics.median(list_tails))]

    # Grab the mode iter using mode_count_num()
    reffArms, countArms = appendage_count(list_arms)
    reffLegs, countLegs = appendage_count(list_legs)
    reffTails, countTails = appendage_count(list_tails)

    iterArms = mode_count(countArms)
    iterLegs = mode_count(countLegs)
    iterTails = mode_count(countTails)

    mode = [reffArms[iterArms], reffLegs[iterLegs], reffTails[iterTails]]

    return mean, median, mode


# Gets the mode of the names of the head types.
def head_count():
    # Gets the json data
    animals = get_data()

    # We know the size has to be 100.
    list_head = [None] * 100

    for i in range(100):
        list_head[i] = animals['animals'][i]['head']

    # Creates new array that'll only have one of each head part.
    reffHead = ["Error, multiple modes for head parts"]  # Error message in case that there are multiple modes,
    # you can't average out the modes if they aren't numbers.

    for i in range(100):
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

        for j in range(100):
            if currHead == list_head[j]:
                countHead[i] += 1

    return reffHead, countHead


def appendage_count(list_append):
    reffAppend = ["Error, multiple modes"]

    for i in range(100):
        currAppend = list_append[i]

        # Checks within reffHead if the head already exists
        for j in range(len(reffAppend)):
            if currAppend == reffAppend[j]:
                break
            elif j == (len(reffAppend) - 1):
                reffAppend.append(currAppend)
                break

    # Goes through the original list and counts the appendages
    countAppend = [0] * len(reffAppend)

    for i in range(len(reffAppend)):
        currAppend = reffAppend[i]

        for j in range(100):
            if currAppend == list_append[j]:
                countAppend[i] += 1

    return reffAppend, countAppend


# Same as head_count, but it'll split the body parts between the hyphen and count them. Name picked for readability.
def body_count():
    # Gets the json data
    animals = get_data()

    # We know the size has to be 100.
    list_body = [None] * 100

    for i in range(100):
        list_body[i] = animals['animals'][i]['body']

    # Creates new array that'll only have one of each body part.
    reffBody = ["Error, multiple modes for body parts"]
    unorganized_reffBody = [""]

    for i in range(100):
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

    unorganized_reffBody.pop(0)  # Removes the first index at the start, kinda an ugly workaround.

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
    num = 0  # The count of the certain body or head part
    iter = 0  # The index of the part within reffHead and reffBody

    for i in range(len(count_list)):
        if num < count_list[i]:
            num = count_list[i]
            iter = i

        # In the case of multiple modes, return error message.
        elif num == count_list[i]:
            iter = 0

    return iter


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
