# Homework 3

The purpose of this homework is:

1. Create 3 routes to your island animal JSON data, one has to be /animals, the other 2 should require a parameter.
2. Containerize your Flask Apps. Be sure to include your json data file in your Container
3. Write an animal_consumer.py

## Description

The latest version is 1.0

The flask script app.py is used to interact with a consumer. The script can fetch all the data for a specific head and 
leg. Furthermore, the script can print out mean, median, mode statistics regarding
each appendage.

## Installation

First, cd into the desired location to clone the repository.

Second, clone and update the repo with the address below onto the local ISP.
```gitexclude
git clone https://github.com/vulong2505/COE-332.git
```
Navigate to the homework3 folder for the relevant scripts.


## Building the Image

To build the image, login into docker with your username and password.
Then, pull the repo to your local ISP.
```dockerfile
docker login
docker pull vulong2505/homework3:1.0
```

Now, move to the appropriate folder and type the follow command to build the image.
```dockerfile
docker run --name "lhv248_homework3" -d -p 5035:5000 vulong2505/homework3:1.0"
```

## Running the Consumer Script

In order to run the animals_consumer.py script, simply run:
```python
python3 animals_consumer.py
```
If the requests library isn't installed, run:
```pip3
pip3 install --user requests
```

## Accessing the Microservices

There are four total microservices within this particular Flask API:
*  localhost:5035/animals --> prints out animals json file
*  localhost:5035/animals/head/&lt;type&gt; --> prints out animals w/ a specific head
*  localhost:5035/animals/legs/&lt;numbers&gt; --> prints out animals w/ a specific number of legs
*  localhost:5035/animals/stats/&lt;part&gt; --> prints out mean, median, mode stats for a specific appendage.

First, to print out the entire animals file, run:
```python
curl localhost:5035/animals
```

Second, to print out animals with a specific head, add a route that includes the desired head. For example:
```python
curl localhost:5035/animals/head/bunny
```

Third, to print out animals with a specific number of legds, add a route that includes the number of legs. For example:
```python
curl localhost:5035/animals/legs/6
```

Fourth, to print out mean, median, mode statistics of a specific appendage (arms, legs, tails, head, body), add a route that includes the desired appendage. For example:
```python
curl localhost:5035/animals/stats/legs
```