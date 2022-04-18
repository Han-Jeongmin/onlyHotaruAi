#! coding:UTF-8
import requests
import json
from BlasRest import BlasRest


class BlasRestFixture(BlasRest):
    
    def __init__(self):
        super().__init__()
        self.URL = self.ROOT_URL + "fixtures/"
    
    
    def search(self, token, project_id):
        params = {'token': token, 'project_id': project_id}
        response = requests.get(self.URL+"search/", params=params, verify=self.VERIFY)
        
        if response.status_code == 200:
            rtn_json = response.json()

        return rtn_json


    def create(self, token, project_id, serial_number):
        print("create")
        payload = {'token': token, 'project_id': project_id, 'serial_number': serial_number, 'status': 2}
        response = requests.post(self.URL+"create/", data=payload, verify=self.VERIFY)
        print(response)
        
        if response.status_code == 200:
            rtn_json = response.json()

        return rtn_json


    def update(self, token, fixture_id, status):
        print('update')
        payload = {'token': token, 'fixture_id': fixture_id, 'status': status}
        response = requests.post(self.URL+"update/", data=payload, verify=self.VERIFY)
        print(response)
        
        if response.status_code == 200:
            rtn_json = response.json()

        return rtn_json


    def delete(self, token, fixture_id):
        print('delete')
        payload = {'token': token, 'fixture_id': fixture_id}
        response = requests.delete(self.URL+"delete/", data=payload, verify=self.VERIFY)
        
        if response.status_code == 200:
            rtn_json = response.json()

        return rtn_json


    def kenpin(self, token, project_id, serial_number):
        payload = {'token': token, 'project_id': project_id, 'serial_number': serial_number}
        print(payload)
        response = requests.post(self.URL+"kenpin/", data=payload, verify=self.VERIFY)
        print(response)
        
        if response.status_code == 200:
            rtn_json = response.json()

        return rtn_json


    def takeout(self, token, project_id, serial_number):
        payload = {'token': token, 'project_id': project_id, 'serial_number': serial_number}
        print(payload)
        response = requests.post(self.URL+"takeout/", data=payload, verify=self.VERIFY)
        print(response)
        
        if response.status_code == 200:
            rtn_json = response.json()

        return rtn_json
        
    def rtn(self, token, project_id, serial_number):
        payload = {'token': token, 'project_id': project_id, 'serial_number': serial_number}
        print(payload)
        response = requests.post(self.URL+"rtn/", data=payload, verify=self.VERIFY)
        print(response)
        
        if response.status_code == 200:
            rtn_json = response.json()

        return rtn_json
  


if __name__ == '__main__':
    fixture_api = BlasRestFixture()
    
    """
    results = fixture_api.search(1, '1')
    print(results)
    for result in results['records']:
       print(result)
    
    
    results = fixture_api.create(1, 12, "まま1まも")
    print(results)
    results = fixture_api.update(1, 11901, 0)
    print(results)

    results = fixture_api.delete(1, 11900)
    print(results)
    

    results = fixture_api.kenpin(1, 12, "aiueoaaa")
    print(results)

    results = fixture_api.takeout(1, 12, "aiueoaaa")
    print(results)
    """
    results = fixture_api.rtn(1, "aiue", "aiueoaaa")
    print(results)
