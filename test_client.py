import socket
from sys import exit

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('127.0.0.1', 12345))

try:
    user_number = int(input("Entrez un nombre : "))
except:
    print("Pas un nombre")
    exit(0)
    
s.send(user_number.to_bytes(2, 'little'))