import requests
import json
url = "http://127.0.0.1:8000/api/students/"

def post_data(url):
    data = {
        "name": "jayesh",
        "roll": -10,
        "city":"indore"
    }
    json_data = json.dumps(data) # convert python object data into json data
    req = requests.post(url=url, data = json_data)
    response = req.json()
    print(response)

post_data(url)

def get_data(url, id=None):
    data = {}
    if id is not None: 
        url += f"{id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"Status Code: {response.status_code}")
 
        try:
            data = response.json()
            # print("Response JSON Data:")
            print(data)
        except ValueError:
            # print("Response is not in JSON format")
            print(response.text)
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

# get_data(url) 
# get_data(url, 1)

def update_data(url):
    data = {
        "id": 1,
        "name": "Ram",
        # "roll": 123,
        "city":"indore"
    }
    json_data = json.dumps(data) # convert python object data into json data
    req = requests.put(url=url, data = json_data)
    response = req.json()
    print(response)

# update_data(url)

def delete_data(url):
    data = {
        "id": 11,
    }
    json_data = json.dumps(data) # convert python object data into json data
    req = requests.delete(url=url, data = json_data)
    response = req.json()
    print(response)

# delete_data(url)