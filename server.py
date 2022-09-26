from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from urllib.parse import urlparse
from urllib.parse import parse_qs
import sqlite3




class Serv(BaseHTTPRequestHandler):

    def do_GET(self):

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers() 
      
            self.wfile.write(bytes("<!DOCTYPE html><html><body><h3>You may now close this window!</h3></body></html>", 'utf-8'))

            params_url = self.path
            parsed_url = urlparse(params_url)


            try:
                captured_code = parse_qs(parsed_url.query)['code'][0]
                captured_state = parse_qs(parsed_url.query)['state'][0]
                captured_realmid = parse_qs(parsed_url.query)['realmId'][0]

                conn = sqlite3.connect('appdata.db')
                c = conn.cursor()
                
                c.execute("UPDATE qbauth SET code=:code", {'code': captured_code})
                conn.commit()

                c.execute("UPDATE qbauth SET state=:state", {'state': captured_state})
                conn.commit()

                c.execute("UPDATE qbauth SET realm=:realm", {'realm': captured_realmid})
                conn.commit()
                conn.close()

            except:
                print('One or more of the URL params doesn\'t exist')




        # with open("params.pickle", "wb") as f:
        #     pickle.dump(parsed_url, f)

httpd = HTTPServer(('localhost', 8000), Serv)

def start_srv():
    httpd.serve_forever()
