import socket

port = 8080
ip_addr = '10.1.1.11'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip_addr, port))  

print(f"Server started at port :{port}")

s.listen(1)

while True:
    
    conn, addr = s.accept()
    
    print(f"Client {addr[0]} is connected")
    
    try:
        user_input_byte_len = int.from_bytes(conn.recv(4), byteorder='big')
        if not user_input_byte_len:
            continue
        
        request = conn.recv(user_input_byte_len).decode('utf-8')
        
        if request == "GET /" or request == "/":
            response = "HTTP/1.0 200 OK\n\n<h1>Hello je suis un serveur HTTP</h1>"
            response_len = int.to_bytes(len(response), 4, byteorder='big')
            
            header = response_len
            sequence = header + response.encode('utf-8')
            
            conn.send(sequence)
        else:
            continue
        
    except socket.error:
        print("Error Occured.")
        break

conn.close()