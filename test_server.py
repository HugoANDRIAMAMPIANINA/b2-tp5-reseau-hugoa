import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 12345))  

s.listen(1)
conn, addr = s.accept()

while True:

    try:
        data = conn.recv(1024)
        print(len(data))
        print(f"Received : {int.from_bytes(data, 'little')}")
        
    except socket.error:
        print("Error Occured.")
        break
