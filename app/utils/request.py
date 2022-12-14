import base64
import subprocess

import requests

from app.read_conf import config

bashCommand = "/home/yank0vy3rdna/yandex-cloud/bin/yc iam create-token"


def get_iap_token():
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode()[:-1]


def send_request_yandex_vision(img):
    response = requests.post('https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze',
                             headers={
                                 'Content-Type': 'application/json',
                                 'Authorization': 'Bearer ' + get_iap_token()
                             },
                             json=get_body_request(
                                 img,
                                 config.yandex_bot.folder_id
                             ))
    if response.status_code != 200:
        raise Exception(response.json())
    faces = response.json()["results"][0]["results"][0]["faceDetection"]["faces"]
    result = []
    for face in faces:
        list_x = [int(vertice["x"]) for vertice in face["boundingBox"]['vertices']]
        list_y = [int(vertice["y"]) for vertice in face["boundingBox"]['vertices']]
        result.append((list_x, list_y))
    return result


def get_body_request(img, folder_id):
    body = {
        "folderId": folder_id,
        "analyze_specs": [{
            "content": encode_file(img),
            "mimeType": "image/png",
            "features": [{
                "type": "FACE_DETECTION",
            }]
        }]
    }
    return body


def encode_file(file_content):
    return base64.b64encode(file_content).decode()
