#! coding:UTF-8
import requests
import json
from blas_rest import BlasRest
from blas_rest import log


class BlasRestImage(BlasRest.BlasRest):
    
    def __init__(self, root_url):
        super().__init__()
        self.URL = root_url + "images/"
    
    
    def download(self, token, item_id, project_image_id=None):
        params = {'token': token, 'item_id': item_id}
        
        if project_image_id != None:
            params['project_image_id'] = project_image_id


        response = requests.get(self.URL+"download/", params=params, verify=self.VERIFY)
                    
        if response.status_code == 200:
            rtn_json = response.json()
        else:
            rtn_json = None
            
        return rtn_json

    
    def upload(self, token, project_id, project_image_id, item_id, image, image_type):
        
        params = {'token': token, 'project_id': project_id, 'project_image_id': project_image_id,
                  'item_id': item_id, 'image': image, 'image_type': image_type}

        response = requests.post(self.URL+"upload/", data=params, verify=self.VERIFY)
        print(response)
        if response.status_code == 200:
            rtn_json = response.json()
        else:
            rtn_json = None
            
        return rtn_json


    def delete(self, token,image_id):
        
        params = {'token': token, 'image_id': image_id}

        response = requests.delete(self.URL+"delete/", data=params, verify=self.VERIFY)

        if response.status_code == 200:
            rtn_json = response.json()
        else:
            rtn_json = None

        return rtn_json

    def url(self, token, item_id, project_image_id):
        params = {'token': token, 'item_id': item_id, 'project_image_id': project_image_id}
        response = requests.get(self.URL+"url/", params=params, verify=self.VERIFY)
                    
        if response.status_code == 200:
            rtn_json = response.json()
        else:
            rtn_json = None
            
        return rtn_json

    def get_img(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.content

        return None
