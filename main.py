import falcon
import random
import json

def generate_rfid_number():
    return ''.join(str(random.choice('0123456789ABCDEF')) for _ in range(24))

def load_rfid_numbers_from_file(file_path):
    with open(file_path, 'r') as file:
        rfid_numbers = [line.strip() for line in file.readlines() if line.strip()]
    return rfid_numbers

# 初期化時にテキストファイルからRFID番号を読み込む
g_rfid_numbers_now = load_rfid_numbers_from_file('RFID.txt')
g_door_lock_status = True

class GetRfidDatas:
    def on_post(self, req, resp):
        global g_rfid_numbers_now
        msg = {
            "rfid_datas": g_rfid_numbers_now
        }
        resp.body = json.dumps(msg)
        resp.status = falcon.HTTP_200

class AddRfidData:
    def on_post(self, req, resp):
        global g_rfid_numbers_now
        new_rfid = generate_rfid_number()
        g_rfid_numbers_now.append(new_rfid)
        msg = {
            "message": "RFID data added",
            "new_rfid": new_rfid
        }
        resp.body = json.dumps(msg)
        resp.status = falcon.HTTP_201

class RemoveRfidData:
    def on_post(self, req, resp):
        global g_rfid_numbers_now
        if g_rfid_numbers_now:
            removed_rfid = g_rfid_numbers_now.pop(0)  # FIFOで削除（最初の要素を削除）
            msg = {
                "message": "RFID data removed",
                "removed_rfid": removed_rfid
            }
        else:
            msg = {
                "message": "No RFID data to remove"
            }
        resp.body = json.dumps(msg)
        resp.status = falcon.HTTP_200

class UnlockDoor:
    def on_post(self, req, resp):
        global g_door_lock_status
        g_door_lock_status = False
        print("LockDoor called: g_door_lock_status set to", g_door_lock_status)
        msg = {
            "result": "unlocked"
        }
        resp.body = json.dumps(msg)
        resp.status = falcon.HTTP_200

class LockDoor:
    def on_post(self, req, resp):
        global g_door_lock_status
        g_door_lock_status = True
        print("LockDoor called: g_door_lock_status set to", g_door_lock_status)
        msg = {
            "result": "locked"
        }
        resp.body = json.dumps(msg)
        resp.status = falcon.HTTP_200

class LockStatus:
    def on_post(self, req, resp):
        global g_door_lock_status
        msg = {
            "result": g_door_lock_status
        }
        resp.body = json.dumps(msg)
        resp.status = falcon.HTTP_200

api = falcon.App()
api.add_route('/get-rfid-datas', GetRfidDatas())
api.add_route('/unlock-door', UnlockDoor())
api.add_route('/add-rfid-data', AddRfidData())
api.add_route('/remove-rfid-data', RemoveRfidData())
api.add_route('/lock-door', LockDoor())
api.add_route('/get-lock-status', LockStatus())