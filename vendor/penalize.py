import json
from datetime import date
import datetime
import os

BLACK_USER = 2
GREY_USER = 1
WHITE_USER = 0

file_path = "./log/users_list.json"
ipblacklist_path = "/etc/apache2/ipblacklist.conf"

def load(req):
    with open(file_path) as file_content:
        list_file = json.load(file_content)
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

        with open(file_path) as file_content:
            data = json.load(file_content)
            temp = data["clients_records"]
            temp.append(new_client)
        write_json(data)


    with open(file_path) as file_content:
        data = json.load(file_content)
        for rec in data["clients_records"]:
            if rec["ip"] == ip:
                rec["score"] = score
                break
        
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
    with open(ipblacklist_path, "a") as file_content:
        file_content.write("\nRequire not ip "+str(req.client_address[0]))
        print(file_content)
        reload_service()

def reload_service():
    os.system("service apache2 reload")

def has_access(req, days_to_unblock, grey_score_max, black_score_max):
    ip = req.client_address[0]
    blocked_date = ""

    with open(file_path) as file_content:
        data = json.load(file_content)
        for rec in data["clients_records"]:
            if rec["ip"] == ip:
                if rec["score"] >= black_score_max:
                    blocked_date = rec["date"]
                break
    

    print(blocked_date)
    if blocked_date:
        if unblock(blocked_date, days_to_unblock, ip, grey_score_max):
            return True
        else:
            return False
    else:
        return True


def unblock(blocked_date, days_to_unblock, ip, grey_score_max):
    blocked_date = datetime.datetime.strptime(blocked_date, '%Y-%m-%d').date()
    date_today = date.today()

    date_diff = abs((date_today - blocked_date).days)
    

    if date_diff >= days_to_unblock:
        with open(ipblacklist_path) as file_content:
            ipblacklist_content = file_content.read()

        ipblacklist_content = ipblacklist_content.split("\n")
        for i,ip_record in enumerate(ipblacklist_content):
            if ip_record.find(ip) != -1:
                ipblacklist_content.pop(i)
                with open(ipblacklist_path, "w") as file_content:
                    file_content.write(list_to_str(ipblacklist_content, "\n"))

                reload_service()
                with open(file_path) as file_content:
                    data = json.load(file_content)
                    for rec in data["clients_records"]:
                        if rec["ip"] == ip:
                            rec["score"] = grey_score_max
                            rec["date"] = str(date.today())
                            break
                    
                write_json(data)
                break
                
    else:
        return False


def list_to_str(arr,char):
    ret = ""

    for i in arr:
        ret += i + char

    return ret
