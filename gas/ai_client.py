# coding:UTF-8
import base64
import sys
import os
import requests
import json
from tqdm import tqdm
import glob


def send_image(image_base64, ext):
    payload = {'base64_image': image_base64, 'ext': ext}
    response = requests.post("http://192.168.1.86:5000", data=payload)

    if response.status_code == 200:
        rtn_json = response.json()
    else:
        rtn_json = None
    
    return rtn_json


def image_file_to_base64(file_path):
    with open(file_path, "rb") as image_file:
        data = base64.b64encode(image_file.read())

    return data.decode('utf-8')


if __name__ == '__main__':

    # 画像ファイルを読み込んでBase64に変換する
    for img in glob.glob(r"20200617120444/*/*.jpeg"):
        print(img)
        base64_img = image_file_to_base64(img)

        rtn = send_image(base64_img, "jpg")

        print(rtn)

        input("press any key")
    
