import json

file_path = "./log/log.json"

def log(req=None, resp=None, req_params=None, is_malicious=None):

    log_data = {'req': {}, 'resp': {}}

    for req_param in req.headers:
        log_data['req'][req_param] = req.headers[req_param]

    log_data['req']['client_address'] = req.client_address

    if is_malicious:
        log_data['req']['is_malicious'] = 1
    else:
        log_data['req']['is_malicious'] = 0

    log_data['req']['location'] = req.path

    if resp:
        for resp_param in resp.headers:
            log_data['resp'][resp_param] = resp.headers[resp_param]

        log_data['resp']['status_code'] = resp.status_code

    if req_params:
        log_data['req']['params'] = req_params


    with open(file_path) as write_file:
        data = json.load(write_file)
        temp = data["log_records"]
        temp.append(log_data)
    write_json(data)


def write_json(data, filename=file_path):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)