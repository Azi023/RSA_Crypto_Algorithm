# interface.py
import PySimpleGUI as sg
from key_generation import generate_keys, save_keys
from encryption_decryption import encrypt_file, decrypt_file
from performance_analysis import measure_performance
import os

def main():
    sg.theme('LightBlue')

    layout = [
        [sg.Text('RSA Encryption Tool')],
        [sg.Text('Select Key Size:'), sg.InputCombo(['1024', '2048', '4096'], key='key_size')],
        [sg.Button('Generate Keys')],
        [sg.Text('_' * 80)],
        [sg.Text('Select File to Encrypt:'), sg.Input(), sg.FileBrowse(key='encrypt_file')],
        [sg.Text('Save Encrypted File As:'), sg.Input('encrypted_file.bin'), sg.FileSaveAs(key='encrypt_output')],
        [sg.Button('Encrypt')],
        [sg.Text('_' * 80)],
        [sg.Text('Select File to Decrypt:'), sg.Input(), sg.FileBrowse(key='decrypt_file')],
        [sg.Text('Select Output Directory:'), sg.Input(), sg.FolderBrowse(key='decrypt_output_dir')],
        [sg.Button('Decrypt')],
        [sg.Text('_' * 80)],
        [sg.Multiline(size=(80, 10), key='output', disabled=True, autoscroll=True)],
        [sg.Button('Exit')]
    ]

    window = sg.Window('RSA Encryption Tool', layout)

    while True:
        event, values = window.read()

        if event in (None, 'Exit'):
            break
        elif event == 'Generate Keys':
            key_size = values['key_size']
            if not key_size:
                window['output'].print("Please select a key size.")
                continue
            try:
                key_size = int(key_size)
                private_key_path = os.path.join('keys', 'private_key.pem')
                public_key_path = os.path.join('keys', 'public_key.pem')
                private_key, public_key = generate_keys(key_size)
                save_keys(private_key, public_key, private_key_path, public_key_path)
                window['output'].print(f"Keys generated and saved to {private_key_path} and {public_key_path}")
            except Exception as e:
                window['output'].print(f"Error generating keys: {e}")
        elif event == 'Encrypt':
            file_path = values['encrypt_file']
            output_path = values['encrypt_output']
            if not file_path:
                window['output'].print("Please select a file to encrypt.")
                continue
            if not output_path:
                window['output'].print("Please select a location to save the encrypted file.")
                continue
            public_key_path = os.path.join('keys', 'public_key.pem')
            try:
                # Measure performance
                _, metrics = measure_performance(encrypt_file, file_path, public_key_path, output_path)
                window['output'].print(f"File encrypted and saved to {output_path}")
                window['output'].print("Encryption Performance Metrics:")
                window['output'].print(f"Elapsed Time: {metrics['elapsed_time']:.4f} seconds")
                window['output'].print(f"CPU Time: {metrics['cpu_time']:.4f} seconds")
                window['output'].print(f"Memory Usage: {metrics['memory_usage']:.2f} MB")
            except Exception as e:
                window['output'].print(f"Error encrypting file: {e}")
        elif event == 'Decrypt':
            file_path = values['decrypt_file']
            output_dir = values['decrypt_output_dir']
            if not file_path:
                window['output'].print("Please select a file to decrypt.")
                continue
            if not output_dir:
                window['output'].print("Please select an output directory for the decrypted file.")
                continue
            private_key_path = os.path.join('keys', 'private_key.pem')
            try:
                # Measure performance
                _, metrics = measure_performance(decrypt_file, file_path, private_key_path, output_dir)
                window['output'].print(f"File decrypted and saved to {output_dir}")
                window['output'].print("Decryption Performance Metrics:")
                window['output'].print(f"Elapsed Time: {metrics['elapsed_time']:.4f} seconds")
                window['output'].print(f"CPU Time: {metrics['cpu_time']:.4f} seconds")
                window['output'].print(f"Memory Usage: {metrics['memory_usage']:.2f} MB")
            except Exception as e:
                window['output'].print(f"Error decrypting file: {e}")
        else:
            window['output'].print(f"Unrecognized event: {event}")

    window.close()

if __name__ == '__main__':
    main()
