import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('10.1.1.11', 12345))  

s.listen(1)
conn, addr = s.accept()

while True:

    try:
        data = conn.recv(1024)
        
        if not data: continue
        
        print(len(data))
        print(f"Received : {int.from_bytes(data, 'big')}")
        
    except socket.error:
        print("Error Occured.")
        break
