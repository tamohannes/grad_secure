import logging
import json

def log(req):

    data = {}
    for cred in req:
        data[cred] = req[cred]

    with open("./log/log2.json", "a") as write_file:
        json.dump(data, write_file)
        write_file.write(",\n")