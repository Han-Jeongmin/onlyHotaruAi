#! coding:UTF-8
import requests
import json
from blas_rest import BlasRest


class BlasRestItem(BlasRest.BlasRest):
    
    def __init__(self, root_url):
        super().__init__()
        self.URL = root_url + "items/"
    
    
    def search(self, token, project_id, fld_list=None, date_dict=None):
        params = {'token': token, 'project_id': project_id}

        if fld_list:
            for fld in fld_list:
                fld_name = fld[0]
                fld_value = fld[1]
                params[fld_name] = fld_value

        if bool(date_dict):
            params["date_field"] = str(json.dumps(date_dict))
            
        response = requests.get(self.URL+"search/", params=params, verify=self.VERIFY)
        
        if response.status_code == 200:
            rtn_json = response.json()
        else:
            rtn_json = None

        return rtn_json


    def create(self, token, project_id, params):
        payload = {'token': token, 'project_id': project_id}
        for param in params:
            payload[param] = params[param]
    
        response = requests.post(self.URL+"create/", data=payload, verify=self.VERIFY)
        
        if response.status_code == 200:
            rtn_json = response.json()
        else:
            rtn_json = None
            
        return rtn_json

    def update(self, token, project_id, item_id, params):
        payload = {'token': token, 'project_id': project_id, 'item_id': item_id}
        for param in params:
            payload[param] = params[param]
    
        response = requests.put(self.URL+"update/", data=payload, verify=self.VERIFY)

        if response.status_code == 200:
            rtn_json = response.json()
        else:
            rtn_json = None
            

        return rtn_json


    def delete(self, token, item_id):
        payload = {'token': token, 'item_id': item_id}
    
        response = requests.post(self.URL+"delete/", data=payload, verify=self.VERIFY)
        
        if response.status_code == 200:
            rtn_json = response.json()
        else:
            rtn_json = None

        return rtn_json


    
    
