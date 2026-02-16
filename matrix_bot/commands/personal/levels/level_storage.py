import json
import os

DATA_DIR = "/code/data"

def _get_path(room_id):
    return os.path.join(DATA_DIR, f"{room_id}-level.json")

def _load_data(room_id):
    path = _get_path(room_id)
    os.makedirs(DATA_DIR, exist_ok=True)  # Ensure data dir exists
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump({}, f)  # create blank JSON file
        return {}
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def _save_data(room_id, data):
    path = _get_path(room_id)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def get_user_data(room_id, user_id):
    data = _load_data(room_id)
    return data.get(str(user_id), {"xp": 0, "messages": 0})

def set_user_data(room_id, user_id, new_data):
    data = _load_data(room_id)
    data[str(user_id)] = new_data
    _save_data(room_id, data)

def get_all_user_data(room_id):
    try:
        return _load_data(room_id)
    except Exception:
        return {}
