# from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
# import json
# from log import log
from vendor.log import log
from vendor.config import get_config
# from vendor.discriminator import * 
# from vendor.discriminator.Discriminator import Gago
# from vendor.discriminator.a import *
import pickle

class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.0'

    def do_GET(self, body=True):
        
        self.load_model()
        print("\n\n**********************************************")
        print(self.is_malicious(self.path))
        print(self.path)
        print("**********************************************\n\n")

        req_header = self.headers

        print(req_header)
        print("\n")
        url = '{}://{}:{}{}'.format(configs["webapp"]["protocol"], configs["webapp"]["host"], configs["webapp"]["port"], self.path)

        resp = requests.get(url, headers=req_header, verify=False)
        log(self, resp)
        
        if self.is_malicious(self.path):
            self.send_response(404)
            self.send_resp_headers(resp)
            self.wfile.write(resp.content)
        else:
            self.send_response(resp.status_code)
            self.send_resp_headers(resp)
            self.wfile.write(resp.content)


    def parse_headers(self):
        req_header = {}
        for line in self.headers:
            line_parts = [o.strip() for o in line.split(':', 1)]
            if len(line_parts) == 2:
                req_header[line_parts[0]] = line_parts[1]
        return self.inject_auth(req_header)
    
    def inject_auth(self, headers):
        headers['Authorizaion'] = 'Bearer secret'
        return headers


    def send_resp_headers(self, resp):
        resp_header = resp.headers
        for key in resp_header:
            if key not in ['Content-Encoding', 'Transfer-Encoding', 'content-encoding', 'transfer-encoding', 'content-length', 'Content-Length']:
                self.send_header(key, resp_header[key])
        self.send_header('Content-Length', len(resp.content))
        self.end_headers()

    def is_malicious(self, inputs):
        variables = inputs.split('&')
        values = variables
        return True if self.loaded_model['model'].predict(values).sum() > 0 else False

    def load_model(self):
        filename = './vendor/discriminator/finalized_model.sav'
        self.loaded_model = pickle.load(open(filename, 'rb'))



def get2Grams(payload_obj):
    '''Divides a string into 2-grams
    
    Example: input - payload: "<script>"
             output- ["<s","sc","cr","ri","ip","pt","t>"]
    '''
    payload = str(payload_obj)
    ngrams = []
    for i in range(0,len(payload)-2):
        ngrams.append(payload[i:i+2])
    return ngrams


if __name__ == '__main__':
    configs = get_config()

    server_address = (configs["gradsecurity"]["host"], int(configs["gradsecurity"]["port"]) )
    httpd = HTTPServer(server_address, ProxyHTTPRequestHandler)
    print('http server is running')
    httpd.serve_forever()
