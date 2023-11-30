import socket
from re import compile

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.1.1.11', 9999))

user_input = input("")
input_byte_len = int.to_bytes(len(user_input),4, byteorder='big')

header = input_byte_len

sequence = header + user_input.encode('utf-8')

s.send(sequence)

response_len = int.from_bytes(s.recv(4), byteorder='big')

print(s.recv(response_len).decode('utf-8'))