import requests
from requests.auth import HTTPBasicAuth


class SheetyManager:
    def __init__(self, url, **kwargs):
        self.url = url
        self.data = {}
        self.sheet_name = url.split('/')[-1]
        self.root = self.sheet_name[:-1]
        self.row_url = None
        if 'auth_method' in kwargs.keys():
            self.auth_method = kwargs['auth_method'].title()
        else:
            self.auth_method = None
        if 'token' in kwargs.keys():
            self.token = kwargs['token']
        else:
            self.token = None
        if 'username' in kwargs.keys():
            self.username = kwargs['username']
        else:
            self.username = None
        if 'password' in kwargs.keys():
            self.password = kwargs['password']
        else:
            self.password = None
        if self.token:
            self.headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            }
        if self.username and self.password:
            self.headers = {
                'Content-Type': 'application/json'
            }

    def get_data(self):
        if self.auth_method is None:
            response = requests.get(url=self.url)
        elif self.auth_method == 'Bearer':
            response = requests.get(url=self.url, headers=self.headers)
        elif self.auth_method == 'Basic':
            response = requests.get(url=self.url, headers=self.headers, auth=HTTPBasicAuth(self.username, self.password))
        return response.json()

    def add_data(self, **kwargs):
        for key, value in kwargs.items():
            self.data.update({key: value})
        payload = {
            self.root: self.data
        }
        if self.auth_method is None:
            response = requests.post(url=self.url, json=payload)
        elif self.auth_method == 'Bearer':
            response = requests.post(url=self.url, headers=self.headers, json=payload)
        elif self.auth_method == 'Basic':
            response = requests.post(url=self.url, headers=self.headers, auth=HTTPBasicAuth(self.username, self.password), json=payload)
        return response.json()

    def edit_data(self, row_id, **kwargs):
        self.row_url = f'{self.url}/{row_id}'
        for key, value in kwargs.items():
            self.data.update({key: value})
        payload = {
            self.root: self.data
        }
        if self.auth_method is None:
            response = requests.put(url=self.row_url, json=payload)
        elif self.auth_method == 'Bearer':
            response = requests.put(url=self.row_url, headers=self.headers, json=payload)
        elif self.auth_method == 'Basic':
            response = requests.put(url=self.row_url, headers=self.headers, auth=HTTPBasicAuth(self.username, self.password), json=payload)
        return response.json()

    def delete_data(self, row_id):
        self.row_url = f'{self.url}/{row_id}'
        if self.auth_method is None:
            response = requests.delete(url=self.row_url)
        elif self.auth_method == 'Bearer':
            response = requests.delete(url=self.row_url, headers=self.headers)
        elif self.auth_method == 'Basic':
            response = requests.delete(url=self.row_url, headers=self.headers, auth=HTTPBasicAuth(self.username, self.password))
        return 'Object Deleted or no such row'