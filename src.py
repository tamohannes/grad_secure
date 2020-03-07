from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import requests
from log import log

class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.0'

    def do_GET(self, body=True):
        url="http://localhost:9000/"
        # req_header = self.parse_headers()
        req_header = self.headers

        log(req_header)
        print(req_header)
        print("\n")

        resp = requests.get(url, headers=req_header, verify=False)

        self.send_response(resp.status_code)
        self.send_resp_headers(resp)
        self.wfile.write(resp.content)


    def parse_headers(self):
        req_header = {}
        for line in self.headers.headers:
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


if __name__ == '__main__':
    server_address = ('127.0.0.1', 8085)
    httpd = HTTPServer(server_address, ProxyHTTPRequestHandler)
    print('http server is running')
    httpd.serve_forever()
