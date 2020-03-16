import json

file_path = "./log/log2.json"

def log(req=None, resp=None):

    log_data = {'req': {}, 'resp': {}}

    for req_param in req.headers:
        log_data['req'][req_param] = req.headers[req_param]

    log_data['req']['client_address'] = req.client_address
    log_data['req']['path'] = req.path

    if resp:
        for resp_param in resp.headers:
            log_data['resp'][resp_param] = resp.headers[resp_param]

        log_data['resp']['status_code'] = resp.status_code

    with open(file_path, "a") as write_file:
        json.dump(log_data, write_file)
        write_file.write(",\n")
