import socket

port = 8080
ip_addr = '127.0.0.1'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip_addr, port))  

print(f"Server started at port :{port}")

s.listen(1)

while True:
    
    conn, addr = s.accept()
    
    print(f"Client {addr[0]} is connected")
    
    try:
        request = conn.recv(1024).decode('utf-8')
        
        if not request:
            continue
        
        request_elements = request.split(" ")
        method, uri = request_elements[0], request_elements[1]
        print(method, uri)
        
        if method == "GET":
            if uri == "/":
                response = "HTTP/1.0 200 OK\n\n<h1>Hello je suis un serveur HTTP</h1>"
                conn.send(response.encode('utf-8'))
                conn.close()
        else:
            continue
        
    except socket.error:
        print("Error Occured.")
        break
