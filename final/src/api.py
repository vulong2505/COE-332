import json
import jobs
import datetime
import redis

from flask import Flask, request, send_file, jsonify
from jobs import q, rd_jobs, rd_raw, rd_images

app = Flask(__name__)


@app.route('/', methods=['GET'])
def help():
    return """
    blah blah blah
    put stuff here
    
    Hello world! \n
    """


# Database Operations ==================================================================================================

@app.route('/data', methods=['GET'])
def get_data():
    data = json.loads(rd_raw.get('Housing Data'))
    return data


def delete_database():
    rd_raw.flushall()

@app.route('/data/load', methods=['GET'])
def load_data():
    delete_database() # Deletes all data on the redis db to start on clean slate.

    with open("Austin_Affordable_Housing.json", "r") as f:
        housing_data = json.load(f)

    rd_raw.set('Housing Data', json.dumps(housing_data, indent=2))

    return "Housing data has been loaded. \n"


# Job Operations =======================================================================================================

# Run a new job based on parameters such as City Amount from $20000 to $150000
# curl -X POST -d '{"parameter": "Zip Code", "start": 78000, "end": 79000}' localhost:5035/run
@app.route('/run', methods=['GET', 'POST'])
def run_job():
    if request.method == 'POST':
        try:
            job = request.get_json(force=True)
        except Exception as e:
            return True, json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})

        return json.dumps(jobs.add_job(str(datetime.datetime.now()), job['parameter'], job['start'], job['end'])) + "\n"

    else:
        return """
    This is a route for POSTing a job to graph a scatterplot of houses by specifying a start/end range for a certain parameter.
    Parameters include: "Zip Code" and "City Amount"
        
    For example, the json arguments may look like this:
                {"parameter": "Zip Code", "start": 78xxx, "end": 78xxx}
                {"parameter": "City Amount", "start": 20000, "end": 150000}
        
    To curl, use the form:
                curl -X POST -d '{"parameter": <parameter>, "start": <start>, "end": <end>}' localhost:5035/run \n
    """


# List past jobs and its status
@app.route('/jobs', methods=['GET'])
def get_jobs():
    redis_dict = {}

    for key in rd_jobs.keys():
        redis_dict[str(key.decode('utf-8'))] = {}
        redis_dict[str(key.decode('utf-8'))]['id'] = rd_jobs.hget(key, 'id').decode('utf-8')
        redis_dict[str(key.decode('utf-8'))]['status'] = rd_jobs.hget(key, 'status').decode('utf-8')
        redis_dict[str(key.decode('utf-8'))]['datetime'] = rd_jobs.hget(key, 'datetime').decode('utf-8')

    return json.dumps(redis_dict, indent=4)


# Download an image from a job
@app.route('/download/<jid>', methods=['GET'])
def download(jid):
    path = f'/app/{jid}.png'

    with open(path, 'wb') as f:
        f.write(rd_images.hget(jid, 'image'))

    return send_file(path, mimetype='image/png', as_attachment=True)


# CRUD Operations ======================================================================================================

# CREATE - Add a new property
# curl localhost:5035/data/add_house -X POST -H "Content-Type: application/json" -d '{"Address": "5812 Berkman Dr","Zip Code": 78723, "Unit Type": "Single Family", "Tenure": "", "City Amount": 0, "Longitude": -97.692, "Latitude": 30.292107, "Property Manager Phone Number": "", "Property Manager Email": ""}'
@app.route('/data/add_house', methods=['POST'])
def add_house():
    housing_data = get_data()

    new_house = request.get_json(force=True)
    new_project_id = len(housing_data) + 3731
    new_address = new_house['Address']
    new_zip = float(new_house['Zip Code'])
    new_unit_type = new_house['Unit Type']
    new_tenure = new_house['Tenure']
    new_city_amount = float(new_house['City Amount'])
    new_longitude = float(new_house['Longitude'])
    new_latitude = float(new_house['Latitude'])
    new_manager_number = new_house['Property Manager Phone Number']
    new_manager_email = new_house['Property Manager Email']

    housing_data.append({"Project ID": new_project_id, "Address": new_address, "Zip Code": new_zip,
                                         "Unit Type": new_unit_type, "Tenure": new_tenure,
                                         "City Amount": new_city_amount, \
                                         "Longitude": new_longitude, "Latitude": new_latitude, \
                                         "Property Manager Phone Number": new_manager_number, \
                                         "Property Manager Email": new_manager_email})

    rd_raw.set('Housing Data', json.dumps(housing_data, indent=2))

    return "New property has been added. \n"


# READ - Print out property data of specific house using project ID
@app.route('/data/get/<Project_ID>', methods=['GET'])
def get_house(Project_ID):
    housing_data = get_data()

    return json.dumps(housing_data)
    # return json.dumps([x for x in housing_data if x['Project ID'] == Project_ID])

# UPDATE: Update house info
@app.route('/data/update/<Project_ID>', methods=['PUT'])
def update_house(Project_ID):
    housing_data = get_data()

    new_house = request.get_json(force=True)
    new_project_id = len(housing_data) + 3731
    new_address = new_house['Address']
    new_zip = float(new_house['Zip Code'])
    new_unit_type = new_house['Unit Type']
    new_tenure = new_house['Tenure']
    new_city_amount = float(new_house['City Amount'])
    new_longitude = float(new_house['Longitude'])
    new_latitude = float(new_house['Latitude'])
    new_manager_number = new_house['Property Manager Phone Number']
    new_manager_email = new_house['Property Manager Email']

    list = [x for (x, i) in enumerate(housing_data) if i['Project ID'] == Project_ID]

    housing_data[list[0]]['Address'] = new_address
    housing_data[list[0]]['Zip Code'] = new_zip
    housing_data[list[0]]['Unit Type'] = new_unit_type
    housing_data[list[0]]['Tenure'] = new_tenure
    housing_data[list[0]]['City Amount'] = new_city_amount
    housing_data[list[0]]['Longitude'] = new_longitude
    housing_data[list[0]]['Latitude'] = new_latitude
    housing_data[list[0]]['Property Manager Phone Number'] = new_manager_number
    housing_data[list[0]]['Property Manager Email'] = new_manager_email

    rd_raw.set('Housing Data', json.dumps(housing_data, indent=2))

    return "Property has been updated. \n"


# DELETE - Delete house info
@app.route('/data/delete/<Project_ID>', methods=['GET', 'DELETE'])
def delete_house(Project_ID):
    housing_data = get_data()

    house_to_delete = [x for x in housing_data if x['Project ID'] == Project_ID]
    rd_raw.delete(housing_data.index(house_to_delete[0]))

    return "Property has been deleted. \n"


# Main =================================================================================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
