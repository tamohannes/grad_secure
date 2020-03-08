import logging
import json

def log(req, resp):

    data = {'req':{},'resp':{}}

    for req_param in req.headers:
        data['req'][req_param] = req.headers[req_param]

    data['req']['client_address'] = req.client_address
    data['req']['path'] = req.path

    for resp_param in resp.headers:
        data['resp'][resp_param] = resp.headers[resp_param]
    
    data['resp']['status_code'] = resp.status_code
    

    with open("./log/log2.json", "a") as write_file:
        json.dump(data, write_file)
        write_file.write(",\n")