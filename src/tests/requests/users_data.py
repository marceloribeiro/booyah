#!/usr/bin/env python

import requests
import os

host = os.environ.get("LOCAL_SERVER", "https://localhost:8000/")
resource = "/users"
headers = {} #{"Authorization": "Bearer YOUR_ACCESS_TOKEN"}
    
data = {"user":
    {"first_name": "Klaus", "last_name": "Magalhaes", "email": "klaus.trabalhando@gmail.com", "password": "change123"}
}
data = {f"user[{key}]": value for key, value in data["user"].items()}


def get_request(id):
    url = host + resource + f"/{id}"
    response = requests.get(url, headers=headers)
    return response

def post_request(data):
    url = host + resource
    response = requests.post(url, data=data, headers=headers)
    return response

def put_request(data, id):
    url = host + resource + f"/{id}"
    response = requests.put(url, data=data, headers=headers)
    return response

def patch_request(data, id):
    url = host + resource + f"/{id}"
    response = requests.patch(url, data=data, headers=headers)
    return response

def delete_request(id):
    url = host + resource + f"/{id}"
    print(url)
    response = requests.delete(url, headers=headers)
    return response

if __name__ == "__main__":
    print("Simulating REST Requests:")

    # POST
    response_post = post_request(data)
    print("POST Response:", response_post.status_code, response_post.content)
    if response_post.status_code != 200:
        exit()

    json_response = response_post.json()
    response_id = json_response[next(iter(json_response))]['id']

    data = data = {"user":
        {"name": "Balduino"}
    }
    data = {f"user[{key}]": value for key, value in data["user"].items()}

    # PUT
    response_put = put_request(data, response_id)
    print("PUT Response:", response_put.status_code, response_put.content)
    if response_put.status_code != 200:
        exit()

    json_response = response_put.json()
    response_id = json_response[next(iter(json_response))]['id']

    # PATCH
    data = data = {"user":
        {"name": "M Balduino"}
    }
    data = {f"user[{key}]": value for key, value in data["user"].items()}
    response_patch = patch_request(data, response_id)
    print("PATCH Response:", response_patch.status_code, response_patch.content)
    if response_patch.status_code != 200:
        exit()

    json_response = response_patch.json()
    response_id = json_response[next(iter(json_response))]['id']
    
    # GET
    response_get = get_request(response_id)
    print("GET Response:", response_get.status_code, response_get.json())
    if response_get.status_code != 200:
        exit()

    json_response = response_get.json()
    response_id = json_response[next(iter(json_response))]['id']
    
    # DELETE
    response_delete = delete_request(response_id)
    print("DELETE Response:", response_delete.status_code, response_delete.text)