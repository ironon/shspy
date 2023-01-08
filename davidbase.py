import json
import pandas as pd
import atexit

def getDefaultDataframe():
    data = {
        "Messages": {
            "Message": [],
            "Member": [],
            "Timestamp": [],
            "Attachments": [],
            "Embeds": []
        },
        "VC": {
            "Member": [],
            "Timestamp": [],
            "Joined": [],## True if joined, False if left.
        }
    }
    return data
with open("data.json", "r") as f:
    text = f.read()
    jsonData = None
    global data
    print(text)
    try:
        jsonData = json.loads(text)
    except json.JSONDecodeError:
        jsonData = getDefaultDataframe()
    print(jsonData)
    data = pd.DataFrame(jsonData["Messages"])
    vcdata = pd.DataFrame(jsonData["VC"])
    

def saveMessage(message):
    messg =[message[key] for key in message]
    data.loc[len(data["Member"])] = messg
    print(data)

def saveVC(message):
    vc = [message[key] for key in message]
    vcdata.loc[len(vcdata["Member"])] = vc
    print(vcdata)

def exit_handler():
    with open("data.json", "w") as f:
        json.dump({
            "Messages": json.loads(data.to_json()),
            "VC": json.loads(vcdata.to_json()),
            }, f, indent=4)

atexit.register(exit_handler)