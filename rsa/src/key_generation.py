# key_generation.py
from Crypto.PublicKey import RSA

def generate_keys(key_size):
    key = RSA.generate(key_size)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def save_keys(private_key, public_key, private_key_path, public_key_path):
    with open(private_key_path, 'wb') as priv_file:
        priv_file.write(private_key)
    with open(public_key_path, 'wb') as pub_file:
        pub_file.write(public_key)
