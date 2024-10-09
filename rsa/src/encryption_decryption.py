# encryption_decryption.py
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
import struct
import os

def encrypt_file(file_path, public_key_path, output_path):
    # Read public key
    recipient_key = RSA.import_key(open(public_key_path, 'rb').read())
    session_key = get_random_bytes(16)  # AES key

    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    encrypted_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    with open(file_path, 'rb') as f_in:
        data = f_in.read()
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)

    # Get the original file name and encode it
    original_file_name = os.path.basename(file_path)
    original_file_name_bytes = original_file_name.encode('utf-8')
    original_file_name_length = len(original_file_name_bytes)

    # Write the encrypted session key, nonce, tag, original file name length, original file name, and ciphertext to the output file
    with open(output_path, 'wb') as f_out:
        # Write lengths as 2-byte unsigned integers
        f_out.write(struct.pack('H', original_file_name_length))
        f_out.write(original_file_name_bytes)
        f_out.write(struct.pack('H', len(encrypted_session_key)))
        f_out.write(encrypted_session_key)
        f_out.write(cipher_aes.nonce)
        f_out.write(tag)
        f_out.write(ciphertext)



def decrypt_file(file_path, private_key_path, output_dir):
    # Read private key
    private_key = RSA.import_key(open(private_key_path, 'rb').read())

    with open(file_path, 'rb') as f_in:
        # Read original file name length and original file name
        original_file_name_length = struct.unpack('H', f_in.read(2))[0]
        original_file_name = f_in.read(original_file_name_length).decode('utf-8')

        # Read encrypted session key length and encrypted session key
        encrypted_session_key_length = struct.unpack('H', f_in.read(2))[0]
        encrypted_session_key = f_in.read(encrypted_session_key_length)

        nonce = f_in.read(16)
        tag = f_in.read(16)
        ciphertext = f_in.read()

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(encrypted_session_key)

    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)

    # Write the decrypted data to the output file with the original file name
    output_path = os.path.join(output_dir, original_file_name)
    with open(output_path, 'wb') as f_out:
        f_out.write(data)
