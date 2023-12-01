import socket
from os.path import isfile, exists
import logging


def file_exists(file_name: str, file_ext: str) -> bool:
    if file_ext == "html":
        if exists(f"./templates/{file_name}") and isfile(f"./templates/{file_name}"):
            return True
        return False
    
    if exists(f"./{file_name}") and isfile(f"./{file_name}"):
        return True
    return False

def get_html_file_content(file_name: str):
    file = open(f'./templates/{file_name}')
    html_content = file.read()
    file.close()
    http_response = 'HTTP/1.0 200 OK\n\n' + html_content
    return http_response

def get_byte_file_content(file_name: bool):
    file = open(f'./{file_name}', 'rb')
    byte_file_content = file.read()
    file.close()
    return byte_file_content


logger = logging.getLogger("colored_logger")
logger.setLevel(logging.INFO)

log_file_path = "./web_serv.log"
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler = logging.FileHandler(log_file_path)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
    
logger.addHandler(console_handler)
logger.addHandler(file_handler)
    
port = 8080
host = '127.0.0.1'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

logger.info(f'Le serveur tourne sur {host}:{port}')


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
                logger.info(f"Le client télécharge le fichier : index.html")
                conn.close()
            else:
                file_name = uri[1:]
                file_ext = file_name.split(".")[1]
                
                http_response = None
                
                if file_exists(file_name, file_ext):
                    if file_ext == "html":
                        http_response = get_html_file_content(file_name)
                        conn.send(http_response.encode('utf-8'))
                    else:
                        http_response = get_byte_file_content(file_name)
                        conn.send(b"HTTP/1.0 200 OK\n")
                        if file_ext == "mp3":
                            conn.send(f"Content-Type: audio/mpeg\n".encode('utf-8'))
                        else:
                            conn.send(f"Content-Type: image/{file_ext}\n".encode('utf-8'))
                        conn.send(b"\n")
                        chunk_size = 1024
                        for i in range(0, len(http_response), chunk_size):
                            conn.send(http_response[i:i+chunk_size])
                        
                    logger.info(f"Le client télécharge le fichier : {file_name}")
                else:
                    http_response = "HTTP/1.0 404 Not Found\n\n"
                    conn.sendall(http_response.encode('utf-8'))
                
                conn.close()
                continue
                
        else:
            continue
        
    except socket.error as e:
        print(e)
        print("Error Occured.")
        break

s.close()