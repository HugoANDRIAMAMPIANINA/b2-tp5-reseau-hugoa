import socket
from os.path import isfile, exists


def file_exists(file_name: str) -> str|bool:
    if exists(f"./templates/{file_name}") and isfile(f"./templates/{file_name}"):
        return True
    return False

def get_html_file_content(file_name: str):
    file = open(f'./templates/{file_name}')
    html_content = file.read()
    file.close()
    http_response = 'HTTP/1.0 200 OK\n\n' + html_content
    return http_response


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
        request = conn.recv(1024).decode('utf-8')
        
        if not request:
            continue
        
        request_elements = request.split(" ")
        method, uri = request_elements[0], request_elements[1]
        
        if method == "GET":
            if uri == "/":
                response = "HTTP/1.0 200 OK\n\n<h1>Hello je suis un serveur HTTP</h1>"
                conn.send(response.encode('utf-8'))
                conn.close()
            else:
                file_name = uri[1:]
                http_response = None
                
                if file_exists(file_name):
                    http_response = get_html_file_content(file_name)
                else:
                    http_response = "HTTP/1.0 404 Not Found\n\n"
                    
                conn.send(http_response.encode('utf-8'))
                conn.close()
        else:
            continue
        
    except socket.error as e:
        print(e)
        print("Error Occured.")
        break

