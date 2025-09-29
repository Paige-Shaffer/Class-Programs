import socket, os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

host = "127.0.0.1"
port = 1337

key = b"Sixteen byte key"

def encrypt(data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(data, AES.block_size)
    return cipher.encrypt(padded_data)

# Replace 'example_file.txt' with your actual file name
filename = "example_file.txt"
with open(filename, "rb") as f:
    file_data = f.read()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    iv = os.urandom(16)
    s.send(iv)
    encrypted = encrypt(file_data, key, iv)
    print(f"Sending encrypted data: {encrypted.hex()}")
    s.sendall(encrypted)