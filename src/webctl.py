import http.server
import socketserver
import sys
import signal
from common.build import *

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 80
CONFIG_FILE_LOCATION = sys.argv[2] if len(sys.argv) > 2 else "config.yaml"
DOCROOT = sys.argv[3] if len(sys.argv) > 3 else "/var/www/html"

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    # set docroot as /var/www/html
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DOCROOT, **kwargs)

    def do_GET(self):
        if self.path == "/info":
            self.get_info()
        elif self.path == "/api/config":
            self.get_file_contents()
        else:
            if self.path == "/":
                self.path = "/index.html"
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

    # API request handler
    def do_POST(self):
        if self.path == "/api/config":
            self.put_file_contents()
        else:
            self.err_not_found()
    
    def get_info(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"BlackBox webctl\n")
        self.wfile.write(b"University of Southampton\n")
        self.wfile.write(b"---------------------------------------------------------\n")
        self.wfile.write(f"Port: {PORT}\n".encode())
        self.wfile.write("Package version: {VER}\n".format(VER=VERSION).encode())
        self.wfile.write(f"Configuration file location: {CONFIG_FILE_LOCATION}\n".encode())
    
    def get_file_contents(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/yaml")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        with open(CONFIG_FILE_LOCATION, "r") as file:
            self.wfile.write(file.read().encode())
    
    def put_file_contents(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        content_length = int(self.headers["Content-Length"])
        with open(CONFIG_FILE_LOCATION, "w") as file:
            file.write(self.rfile.read(content_length).decode())

    def err_not_found(self):
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"404 NOT FOUND")

def signal_handler(sig, frame):
    print("\nReceived SIGTERM, shutting down server")
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)

try:
    with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
        print("Serving at port", PORT)
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\nExiting due to keyboard interrupt.")
