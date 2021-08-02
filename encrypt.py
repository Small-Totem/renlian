import json
#from pathlib import Path
import os
from secrets import token_bytes

def random_key(length):
    key = token_bytes(nbytes=length)
    key_int = int.from_bytes(key, 'big')
    return key_int
def encrypt(raw):
    raw_bytes = raw.encode()
    raw_int = int.from_bytes(raw_bytes, 'big')
    key_int = random_key(len(raw_bytes))
    return raw_int ^ key_int, key_int
def decrypt(encrypted, key_int):
    decrypted = encrypted ^ key_int
    length = (decrypted.bit_length() + 7) // 8
    decrypted_bytes = int.to_bytes(decrypted, length, 'big')
    return decrypted_bytes.decode()

'''
def encrypt_file(path, key_path=None, *, encoding='utf-8'):
    path = Path(path)
    cwd = path.cwd() / path.name.split('.')[0]
    path_encrypted = cwd / path.name
    if key_path is None:
        key_path = cwd / 'key'
    if not cwd.exists():
        cwd.mkdir()
        path_encrypted.touch()
        key_path.touch()

    with path.open('rt', encoding=encoding) as f1, \
            path_encrypted.open('wt', encoding=encoding) as f2, \
            key_path.open('wt', encoding=encoding) as f3:
        encrypted, key = encrypt(f1.read())
        json.dump(encrypted, f2)
        json.dump(key, f3)

def decrypt_file(path_encrypted, key_path=None, *, encoding='utf-8'):
    path_encrypted = Path(path_encrypted)
    cwd = path_encrypted.cwd()
    path_decrypted = cwd / 'decrypted'
    if not path_decrypted.exists():
        path_decrypted.mkdir()
        path_decrypted /= path_encrypted.name
        path_decrypted.touch()
    if key_path is None:
        key_path = cwd / 'key'
    with path_encrypted.open('rt', encoding=encoding) as f1, \
            key_path.open('rt', encoding=encoding) as f2, \
            path_decrypted.open('wt', encoding=encoding) as f3:
        decrypted = decrypt(json.load(f1), json.load(f2))
        f3.write(decrypted)
'''

#
def write_with_encrypt(target_path, file_name, text, key_path=None, *, encoding='utf-8'):
    if key_path is None:
        key_path = target_path + 'key'
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    with open(target_path+file_name, 'wt', encoding=encoding) as f2, \
            open(key_path, 'wt', encoding=encoding) as f3:
        encrypted, key = encrypt(text)
        json.dump(encrypted, f2)
        json.dump(key, f3)


def read_with_decrypt(target_path, file_name, key_path=None, *, encoding='utf-8'):
    if key_path is None:
        key_path = target_path + 'key'
    with open(target_path+file_name, 'rt', encoding=encoding) as f1, \
            open(key_path, 'rt', encoding=encoding) as f2:
        decrypted = decrypt(json.load(f1), json.load(f2))
    return decrypted
