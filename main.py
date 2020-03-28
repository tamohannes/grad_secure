from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
from vendor.log import log
from vendor.config import get_config
from vendor.helper import is_blocking, penalize, has_access, block_ip
import pickle
import pandas as pd
import random
import urllib.parse
import time


class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.0'

    def do_GET(self, body=True):

        self.load_model()

        # print("\n\n**********************************************")
        # print(self.is_malicious(self.path))
        # print("**********************************************\n\n")

        req_header = self.headers

        url = '{}://{}:{}{}'.format(configs["webapp"]["protocol"],
                                    configs["webapp"]["host"], configs["webapp"]["port"], self.path)
        resp = None

        if self.is_malicious(self.path):
            score = penalize(self)

            if is_blocking(score, configs["score_restrictions"]["gray_client_score_max"], configs["score_restrictions"]["black_client_score_max"]):
                block_ip(self)
                self.send_error(
                    400, message="Ok, that's enough, you are in the Black list")
            else:
                self.send_error(400, message=self.make_fun(
                )+", It seems like an "+self.type_of_attack(self.path))
        else:
            if has_access(self, configs["score_restrictions"]["days_to_unblock"], configs["score_restrictions"]["gray_client_score_max"], configs["score_restrictions"]["black_client_score_max"]):
                resp = requests.get(url, headers=req_header, verify=False)
                self.send_response(resp.status_code)
                self.send_resp_headers(resp)
                self.wfile.write(resp.content)
            else:
                self.send_error(400, message="You'r still in the Black list")

        log(self, resp)

    def do_POST(self, body=True):

        self.load_model()
        content_length = int(self.headers['Content-Length'])
        content = self.rfile.read(content_length)
        content_parsed = urllib.parse.parse_qs(content)

        content_dict, is_malicious = self.parse_content(content_parsed)

        # print("\n\n**********************************************")
        # print(is_malicious)
        # print("**********************************************\n\n")
        req_header = self.headers

        url = '{}://{}:{}{}'.format(configs["webapp"]["protocol"],
                                    configs["webapp"]["host"], configs["webapp"]["port"], self.path)
        resp = None

        if is_malicious:
            score = penalize(self)
            if is_blocking(score, configs["score_restrictions"]["gray_client_score_max"], configs["score_restrictions"]["black_client_score_max"]):
                block_ip(self)
                self.send_error(
                    400, message="Ok, that's enough, you are in the Black list")
            else:
                self.send_error(400, message=self.make_fun(
                )+", It seems like an "+self.type_of_attack(self.path))
        else:
            if has_access(self, configs["score_restrictions"]["days_to_unblock"], configs["score_restrictions"]["gray_client_score_max"], configs["score_restrictions"]["black_client_score_max"]):
                start = time.time()

                resp = requests.post(url, data=content_dict,
                                     headers=req_header, verify=False)

                end = time.time()
                print("\n\n\n\n\n")
                print(end - start)

                self.send_response(resp.status_code)
                self.send_resp_headers(resp)
                self.wfile.write(resp.content)
            else:
                self.send_error(400, message="You are in the Black list")

        log(self, resp, content_dict)

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
            if key not in ['Server', 'Content-Encoding', 'Transfer-Encoding', 'content-encoding', 'transfer-encoding', 'content-length', 'Content-Length']:
                # print(resp_header[key])
                self.send_header(key, resp_header[key])
        self.send_header('Content-Length', len(resp.content))
        # self.send_header('Server',resp.headers["Server"])

        self.end_headers()

    def is_malicious(self, inputs):
        variables = inputs.split('&')
        values = variables
        return True if self.loaded_model['model'].predict(values).sum() > 0 else False

    def load_model(self):
        filename = './vendor/discriminator/finalized_model.sav'
        self.loaded_model = pickle.load(open(filename, 'rb'))

    def type_of_attack(self, input):
        sql_keywords = pd.read_csv(
            './vendor/discriminator/data/SQLKeywords.txt', index_col=False)
        js_keywords = pd.read_csv(
            './vendor/discriminator/data/JavascriptKeywords.txt', index_col=False)

        sql_keyword = 0
        js_keyword = 0

        for keyword in sql_keywords['Keyword']:
            res = str(input).lower().find(str(keyword).lower())
            if res >= 0:
                sql_keyword += 1

        for keyword in js_keywords['Keyword']:
            res = str(input).lower().find(str(keyword).lower())
            if res >= 0:
                js_keyword += 1

        return "SQL" if sql_keyword > js_keyword else "XSS"

    def make_fun(self):
        responses = ["Oh really? Come on", "You must be kidding", "Cant touch this", "Ok you are not playing well", "Is that all you can ?",
                     "Woh, I though you can do better", "That doesnt seem to be cool", "Try harded", "Lets try again, has asenq angleren chgiten sranq", "I am disapointed"]
        return random.choice(responses)

    def parse_content(self, content):
        is_malicious = False
        pair_dic = {}

        for pair in content:

            key = pair.decode()
            if self.is_malicious(key):
                is_malicious = True
                break
            else:
                values = []
                for value_it in content[pair]:
                    value_cont = value_it.decode()
                    if not self.is_malicious(value_cont):
                        values.append(value_cont)
                    else:
                        is_malicious = True
                        break

            if not is_malicious:
                pair_dic[key] = values
            else:
                is_malicious = True
                break

        return pair_dic, is_malicious


def get2Grams(payload_obj):
    payload = str(payload_obj)
    ngrams = []
    for i in range(0, len(payload)-2):
        ngrams.append(payload[i:i+2])
    return ngrams


if __name__ == '__main__':
    configs = get_config()

    server_address = (configs["gradsecurity"]["host"],
                      int(configs["gradsecurity"]["port"]))
    httpd = HTTPServer(server_address, ProxyHTTPRequestHandler)
    print('http server is running')
    httpd.serve_forever()
