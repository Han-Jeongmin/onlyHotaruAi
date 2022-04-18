#! coding:UTF-8
import requests
import json
from blas_rest import BlasRest


class BlasRestAuth(BlasRest.BlasRest):
    
    def __init__(self, root_url):
        super().__init__()
        self.URL = root_url + "auth/"
    

    def login(self, user_name, password):
        payload = {'name': user_name, 'password': password}
        response = requests.post(self.URL+"login/", data=payload, verify=self.VERIFY)

        if response.status_code == 200:
            rtn_json = response.json()

        return rtn_json


if __name__ == '__main__':
    fixture_api = BlasRest.BlasRestAuth()
    
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
    results = fixture_api.login("konishiadmin", "afd0279c")
    print(results)
