# Homework 2

The purpose of this homework is:

1. Write one new feature into the read_animals.py script.
2. Write a unit test for your new feature in read_animals.py
3. Write a Dockerfile to containerize both scripts.
4. Write a reasonable README.md for your repository.

## Description

The latest version is 1.2.

The generate_animals script populates animals.json with animals of differing heads, bodies, arms, legs, and tails.

The read_animals script randomly displays an animal from the json file. It also shows the mean, median, and mode number of 
arms, legs, and tails. Furthermore, the script reads out the most common head and body parts.

## Installation

First, cd into the desired location to clone the repository.

Second, clone and update the repo with the address below onto the local ISP.
```gitexclude
git clone https://github.com/vulong2505/COE-332.git
```
Navigate to the homework2 folder for the relevant scripts.

## Running the Scripts

First, cd into the COE-332 repository and the homework 2 folder.

Then, run the scripts directly from the terminal using "python3".
```python
python3 generate_animals.py # Creates an animal.json
python3 read_animals.py # Reads that json
python3 unittest_animals # Unit test for read_animals
```

## Building the Image

To build the image, login into docker with your username and password.
Then, pull the repo to your local ISP.
```python
docker login
docker pull vulong2505/homework2:1.2
```

Now, move to the appropiate folder and type the follow command to build the image.
```python
docker run --rm -it vulong2505/homework2:1.2 /bin/bash
```


## Running Scripts inside Container

First, cd into the /code folder which contains all the scripts.
```python
cd /code
```


Then, type the command below to run generate_animals.py within the container:
```python
python3 generate_animals.py
```
This will generate a new animals.json.

Finally, type this to run read_animals.py. 
```python
python3 read_animals.py
```
The program may spit out an error message due to having multiple modes in appendages (arms, legs, tails);
this is a byproduct of the .mode() method in the statistics library. Then, just run generate_animals.py again for a 
new animals.json.

## Unit Tests

The unit tests is also built into the container and located within the /code folder. Type the following command:
```python
python3 unittest_animals.py
```
The unit test may give out an error if there are multiple modes in the appendages