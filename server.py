import falcon
import json
import requests

ANDROID_API_URL = 'http://192.168.1.105:8080'
NOTIFY_URL = 'http://example.com/notify'

class GetRfidData:
    def on_post(self, req, resp):
        response = requests.get(f'{ANDROID_API_URL}/get-rfid-data')
        rfid_data = response.json()
        resp.body = json.dumps(rfid_data)
        resp.status = falcon.HTTP_200

class UnlockDoor:
    def __init__(self):
        self.initial_rfid_data = []

    def on_post(self, req, resp):
        # 開始時のRFIDデータを取得して保存する
        rfid_response = requests.get(f'{ANDROID_API_URL}/get-rfid-data')
        self.initial_rfid_data = rfid_response.json()

        # ドアをアンロックする
        response = requests.post(f'{ANDROID_API_URL}/unlock-door')
        result = response.json()

        resp.body = json.dumps(result)
        resp.status = falcon.HTTP_200

class DoorClosed:
    def __init__(self, unlock_door_handler):
        self.unlock_door_handler = unlock_door_handler

    def on_post(self, req, resp):
        # 閉まった時のRFIDデータを取得する
        rfid_response = requests.get(f'{ANDROID_API_URL}/get-rfid-data')
        final_rfid_data = rfid_response.json()

        # 開始時と閉まった時のRFIDデータの差分を計算する
        initial_set = set(self.unlock_door_handler.initial_rfid_data)
        final_set = set(final_rfid_data)
        removed_rfid_data = list(initial_set - final_set)

        # 減ったIDを特定のアドレスに送信する
        raw_json = json.dumps(removed_rfid_data)
        print("Door closed notification received:", raw_json)
        try:
            response = requests.post(NOTIFY_URL, data=raw_json, headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                resp.body = json.dumps({"status": "success"})
            else:
                resp.body = json.dumps({"status": "failed", "reason": response.text})
        except Exception as e:
            resp.body = json.dumps({"status": "error", "message": str(e)})
        resp.status = falcon.HTTP_200
        print(">>DoorClosed")

class GetLockStatus:
    def on_post(self, req, resp):
        response = requests.get(f'{ANDROID_API_URL}/is-door-locked')
        result = response.json()
        resp.body = json.dumps(result)
        resp.status = falcon.HTTP_200

app = falcon.App()
unlock_door_handler = UnlockDoor()
door_closed_handler = DoorClosed(unlock_door_handler)

app.add_route('/get-rfid-datas', GetRfidData())
app.add_route('/unlock-door', unlock_door_handler)
app.add_route('/door-closed', door_closed_handler)
app.add_route('/get-lock-status', GetLockStatus())

from wsgiref import simple_server
server = simple_server.make_server('0.0.0.0', 8000, app)
print(">>Start Serving")
server.serve_forever()