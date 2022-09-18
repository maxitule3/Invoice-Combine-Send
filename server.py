from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json
import pickle
from urllib.parse import urlparse
from urllib.parse import parse_qs




class Serv(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path.endswith('/index'):

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()        
            self.wfile.write(bytes("<!DOCTYPE html><html><body><h3>You may now close this window!</h3></body></html>", 'utf-8'))

            params_url = self.path
            parsed_url = urlparse(params_url)

        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()        
            self.wfile.write(bytes("<!DOCTYPE html><html><body><h3>You may now close this window!</h3></body></html>", 'utf-8'))

            params_url = self.path
            parsed_url = urlparse(params_url)




        # with open("params.pickle", "wb") as f:
        #     pickle.dump(parsed_url, f)

httpd = HTTPServer(('localhost', 8000), Serv)

def start_srv():
    httpd.serve_forever()
