# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer

host_name = "10.1.1.11"
server_port = 8080

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        
def run():
    port = 8080
    server_address = ('', port)
    web_server = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Serveur lancé sur le port :{port}")
    web_server.serve_forever()

if __name__ == '__main__':
    run()