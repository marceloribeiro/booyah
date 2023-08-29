#!/usr/bin/env python

import requests
import os

host = os.environ.get("LOCAL_SERVER", "http://localhost:8000")
resource = "/users"
headers = {} #{"Authorization": "Bearer YOUR_ACCESS_TOKEN"}
    
create_params = {
    "user": {
        "name": "Klaus Magalhães",
        "not_existing_field": "nothing",
        "email": "klaus.trabalhando@gmail.com",
        "password": "change123"
    }
}

put_params = {
    "user": {
        "name": "K Balduino"
    }
}

patch_params = {
    "user": {
        "name": "M Balduino"
    }
}

class UsersControllerRequests:
    def __init__(self, request_format='data'):
        self.request_format = request_format

    def post_request(self):
        data = create_params
        if self.request_format == 'data':
            data = {f"user[{key}]": value for key, value in data["user"].items()}
            return requests.post(host + resource, data=data, headers=headers)
        else:
            return requests.post(host + resource, json=data, headers=headers)

    def member_url(self):
        return host + resource + f"/{self.id}"

    def get_request(self):
        return requests.get(self.member_url(), headers=headers)

    def put_request(self):
        data = put_params
        if self.request_format == 'data':
            data = {f"user[{key}]": value for key, value in data["user"].items()}
            return requests.put(self.member_url(), data=data, headers=headers)
        else:
            return requests.put(self.member_url(), json=data, headers=headers)

    def patch_request(self):
        data = patch_params
        if self.request_format == 'data':
            data = {f"user[{key}]": value for key, value in data["user"].items()}
            return requests.patch(self.member_url(), data=data, headers=headers)
        else:
            return requests.patch(self.member_url(), json=data, headers=headers)

    def delete_request(self):
        return requests.delete(self.member_url(), headers=headers)
    
    def execute_all(self):
        # POST
        response_post = self.post_request()
        print("POST Response: ", response_post.status_code, response_post.content)
        if response_post.status_code != 200:
            exit()
        json_response = response_post.json()
        self.id = json_response[next(iter(json_response))]['id']

        # PUT
        response_put = self.put_request()
        print("PUT Response:", response_put.status_code, response_put.content)
        if response_put.status_code != 200:
            exit()
        json_response = response_put.json()
        self.id = json_response[next(iter(json_response))]['id']

        # PATCH
        response_patch = self.patch_request()
        print("PATCH Response:", response_patch.status_code, response_patch.content)
        if response_patch.status_code != 200:
            exit()
        json_response = response_patch.json()
        self.id = json_response[next(iter(json_response))]['id']
        
        # GET
        response_get = self.get_request()
        print("GET Response:", response_get.status_code, response_get.json())
        if response_get.status_code != 200:
            exit()
        json_response = response_get.json()
        self.id = json_response[next(iter(json_response))]['id']
        
        # DELETE
        response_delete = self.delete_request()
        print("DELETE Response:", response_delete.status_code, response_delete.text)


if __name__ == "__main__":
    print("Simulating REST Requests:")

    print('** URL ENCODED FORMAT **')
    users_request = UsersControllerRequests('data')
    users_request.execute_all()

    print('**JSON FORMAT**')
    users_request = UsersControllerRequests('json')
    users_request.execute_all()