import socket
from sys import exit

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('10.1.1.11', 12345))

try:
    user_number = input("Entrez un nombre : ")
except:
    print("Pas un nombre")
    exit(0)
    
# s.send(user_number.to_bytes(user_number.bit_length(), 'big'))
s.send(user_number.encode())
# print(f"You send the number : {user_number} with {user_number.bit_length()} number of bit")
print(f"You send the number : {user_number} with {len(user_number)} number of bit")