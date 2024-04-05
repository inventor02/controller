import http.server
import socketserver
import sys
import signal
from common.build import *

PORT = 8000

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/info":
            self.get_info()
        else:
            self.err_not_found()

    # API request handler
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
    
    def get_info(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"BlackBox webctl\n")
        self.wfile.write(b"University of Southampton\n")
        self.wfile.write(b"---------------------------------\n")
        self.wfile.write("Package version:            {VER}\n".format(VER=VERSION).encode())

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
