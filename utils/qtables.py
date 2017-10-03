from array import array
import base64
from hashlib import sha1
import json
import os

from PIL import Image


def extract_qtable(path):
    with Image.open(path) as im:
        qtable = im.quantization
    return {int(k): list(v) for k, v in qtable.items()}


def generate_qtable_hash(qtable):
    hash = sha1(json.dumps(qtable).encode('utf-8'))
    return base64.b64encode(hash.digest(), '-_')[:3].decode('utf-8')


def save_qtable(path):
    qtable = extract_qtable(path)
    hash = generate_qtable_hash(qtable)
    path = os.path.join(os.path.dirname(__file__), '..', 'qtables', hash)
    with open(path, 'w') as f:
        f.write(json.dumps(qtable))
    return hash


def load_qtable(hash):
    path = os.path.join(os.path.dirname(__file__), '..', 'qtables', hash)
    with open(path, 'r') as f:
        data = json.loads(f.read())
    return {int(k): v for k, v in data.items()}
