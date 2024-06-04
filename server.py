import falcon
import json
import requests

ANDROID_API_URL = 'http://192.168.1.105:8080'

class GetRfidData:
    def on_post(self, req, resp):
        response = requests.post(f'{ANDROID_API_URL}/get-rfid-datas')
        rfid_data = response.json()
        resp.body = json.dumps(rfid_data)
        resp.status = falcon.HTTP_200

class UnlockDoor:
    def on_post(self, req, resp):
        response = requests.post(f'{ANDROID_API_URL}/unlock-door')
        result = response.json()
        resp.body = json.dumps(result)
        resp.status = falcon.HTTP_200

class LockDoor:
    def on_post(self, req, resp):
        response = requests.post(f'{ANDROID_API_URL}/lock-door')
        result = response.json()
        resp.body = json.dumps(result)
        resp.status = falcon.HTTP_200

class GetLockStatus:
    def on_post(self, req, resp):
        response = requests.post(f'{ANDROID_API_URL}/get-lock-status')
        result = response.json()
        resp.body = json.dumps(result)
        resp.status = falcon.HTTP_200

app = falcon.App()
app.add_route('/get-rfid-datas', GetRfidData())
app.add_route('/unlock-door', UnlockDoor())
app.add_route('/lock-door', LockDoor())
app.add_route('/get-lock-status', GetLockStatus())


from wsgiref import simple_server
server = simple_server.make_server('0.0.0.0', 8000, app)
server.serve_forever()