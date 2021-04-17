import json
import redis
import statistics
import datetime as dt
import os

from flask import Flask, request

app = Flask(__name__)

# Pass IP as an Environmental Variable
# redis_ip = os.environ.get('REDIS_IP')
#
# if not redis_ip:
#     raise Exception()

rd = redis.StrictRedis(host='10.104.131.15', port=6379, db=0)


@app.route('/', methods=['GET'])
def hello_world():
    return "Hello! \n"


@app.route('/animals', methods=['GET'])
def get_animals():
    return json.dumps(get_data())


# Updates the redis server w/ the latest json
def update_redis():
    with open("/app/data_file.json", "r") as f:  # the full path is in /app/ within the docker container
        animal_data = json.load(f)

    rd.set('animals', json.dumps(animal_data, indent=2))

    return '', 204


# Gets the data from the server
def get_data():
    update_redis()
    animals = json.loads(rd.get('animals').decode('utf-8'))
    return animals


# curl "localhost:5035/animals/query?start='2021-03-27_00:00:00.0'&end='2021-03-29_00:00:00.0'"
@app.route('/animals/query', methods=['GET'])
def query_date_range():
    start = request.args.get('start')
    end = request.args.get('end')
    start_date = dt.datetime.strptime(start, "'%Y-%m-%d_%H:%M:%S.%f'")
    end_date = dt.datetime.strptime(end, "'%Y-%m-%d_%H:%M:%S.%f'")

    json_data = get_data()

    output = []

    for index in range(len(json_data['animals'])):
        current_date = dt.datetime.strptime(json_data['animals'][index]['timestamp'], '%Y-%m-%d %H:%M:%S.%f')

        if start_date <= current_date <= end_date:
            uid = json_data['animals'][index]['uid']
            head = json_data['animals'][index]['head']
            body = json_data['animals'][index]['body']
            arms = json_data['animals'][index]['arms']
            legs = json_data['animals'][index]['legs']
            tails = json_data['animals'][index]['tails']
            timestamp = json_data['animals'][index]['timestamp']

            output.append({'uid': uid, 'head': head, 'body': body, 'arms': arms, 'legs': legs, 'tails': tails,
                           'timestamp': timestamp})

    return json.dumps(output)


@app.route('/animals/uid/<uid>', methods=['GET'])
def uid_search(uid):
    json_data = get_data()

    output = []

    for index in range(len(json_data['animals'])):
        current_animal_uid = json_data['animals'][index]['uid']

        if current_animal_uid == uid:
            uid = json_data['animals'][index]['uid']
            head = json_data['animals'][index]['head']
            body = json_data['animals'][index]['body']
            arms = json_data['animals'][index]['arms']
            legs = json_data['animals'][index]['legs']
            tails = json_data['animals'][index]['tails']
            timestamp = json_data['animals'][index]['timestamp']

            output.append({'uid': uid, 'head': head, 'body': body, 'arms': arms, 'legs': legs, 'tails': tails,
                           'timestamp': timestamp})

    return json.dumps(output)


# curl "localhost:5035/animals/uidedit?uid=5bf28cd4-9746-46c5-8953-4b53482f89fb&part=arms&edit=6"
# The queries took the single quotations ' ' for some reason, so remove it.
@app.route('/animals/uidedit', methods=['GET'])
def uid_edit():  # (uid, part, edit)
    uid = request.args.get('uid')
    part = request.args.get('part')
    edit = request.args.get('edit')

    # print(type(uid))
    # print(type(part))
    # print(type(edit))

    json_data = get_data()

    if part in ['arms', 'legs', 'tails']:  # The function is not even hitting this if statement??? part is a type str.
        edit = int(edit)
        # print("IM HERE!")
        # print(type(edit))
        # print(edit)

    for index in range(len(json_data['animals'])):
        current_animal_uid = json_data['animals'][index]['uid']
        # print(current_animal_uid)
        # print(type(current_animal_uid))

        if current_animal_uid == uid:  # It never even hit the if statement to find the uid?
            print("I found the correct uid!")
            json_data['animals'][index][part] = edit
            print(json_data['animals'][index][part])

    with open('data_file.json', 'w') as f:
        json.dump(json_data, f, indent=2)

    update_redis()  # Update

    return '', 204  # Change later to uid_search(uid) or something


# curl "localhost:5035/animals/querydelete?start='2021-03-27_00:00:00.0'&end='2021-03-29_00:00:00.0'"
@app.route('/animals/querydelete', methods=['GET'])
def query_date_range_delete():  # (start, end)
    start = request.args.get('start')
    end = request.args.get('end')
    start_date = dt.datetime.strptime(start, "'%Y-%m-%d_%H:%M:%S.%f'")
    end_date = dt.datetime.strptime(end, "'%Y-%m-%d_%H:%M:%S.%f'")

    json_data = get_data()

    for a in reversed(json_data['animals']):
        current_date = dt.datetime.strptime(a['timestamp'], '%Y-%m-%d %H:%M:%S.%f')

        if start_date <= current_date <= end_date:
            json_data['animals'].remove(a)

    with open('data_file.json', 'w') as f:
        json.dump(json_data, f, indent=2)

    update_redis()

    return '', 204


@app.route('/animals/get_leg_average', methods=['GET'])
def get_avg_legs():
    json_data = get_data()

    list_legs = []


    for index in range(len(json_data['animals'])):
        list_legs.append(json_data['animals'][index]['legs'])

    return json.dumps(statistics.mean(list_legs))


@app.route('/animals/get_length', methods=['GET'])
def length_json():
    json_data = get_data()

    length_json = len(json_data['animals'])

    return json.dumps(length_json)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')