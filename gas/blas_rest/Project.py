#! coding:UTF-8
import requests
import json
from blas_rest import BlasRest


class BlasRestProject(BlasRest.BlasRest):
    
    def __init__(self, root_url):
        super().__init__()
        self.URL = root_url + "projects/"
    
    
    def search(self, token, name=None):
        params = {'token': token}
        if name != None:
            params['name'] = name

        response = requests.get(self.URL+"search/", params=params, verify=self.VERIFY)
        
        if response.status_code == 200:
            rtn_json = response.json()
        else:
            rtn_json = None
            
        return rtn_json
