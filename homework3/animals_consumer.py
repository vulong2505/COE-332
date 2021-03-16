import requests

response1 = requests.get(url="http://localhost:5035/animals")

print(response1.status_code)
print(response1.json())
print(response1.headers)

response2 = requests.get(url="http://localhost:5035/animals/head/bunny")

print(response2.status_code)
print(response2.json())
print(response2.headers)

response3 = requests.get(url="http://localhost:5035/animals/legs/6")

print(response3.status_code)
print(response3.json())
print(response3.headers)

response4 = requests.get(url="http://localhost:5035/animals/stats/legs")

print(response4.status_code)
print(response4.json())
print(response4.headers)