import json
from datetime import date

BLACK_USER = 2
GREY_USER = 1
WHITE_USER = 0

file_path = "./log/users_list.json"

def load(req):
    with open(file_path) as write_file:
        list_file = json.load(write_file)
    return list_file, req.client_address[0]


def penalize(req):
    list_file, ip = load(req)
    ip = req.client_address[0]

    client = {}
    for record in list_file["clients_records"]:
        if ip == record["ip"]:
            client = record
            break

    # if user has record
    if client:
        score = client["score"] + 1
    else:
        score = 1

        new_client = {
            "ip": ip,
            "score": score,
            "date": str(date.today())
        }

        with open(file_path) as write_file:
            data = json.load(write_file)
            temp = data["clients_records"]
            temp.append(new_client)
        write_json(data)


    with open(file_path) as write_file:
        data = json.load(write_file)
        for rec in data["clients_records"]:
            if rec["ip"] == ip:
                rec["score"] = score
        
    write_json(data)

    return score
    # get_status(score, grey_score_max, black_score_max)


def write_json(data, filename=file_path):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def is_blocking(score, grey_score_max, black_score_max):
    if get_status(score, grey_score_max, black_score_max) == BLACK_USER:
        return True
    else:
        return False


def get_status(score, grey_score_max, black_score_max):
    if score < grey_score_max:
        return WHITE_USER
    elif score >= grey_score_max and score < black_score_max:
        return GREY_USER
    else:
        return BLACK_USER


def block_ip(req):
    with open("/etc/apache2/ipblacklist.conf", "a") as myfile:
        myfile.write("\nRequire not ip "+str(req.client_address[0]))
        print("*******************\n")
        print(myfile)
        print("*********************")

def is_unblocking(req, days_to_ublock):
    True
