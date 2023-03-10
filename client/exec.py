# Read the contents of src.py and execute them as a python program.
# This lets us arbitrarily overwrite our program as desired
from pathlib import Path
while True:
    contents = Path(".", "src.py").read_text()
    try:
        exec(contents)
    except Exception as e:
        if e is SystemExit:
            break
        else:
            continue
# https://stackoverflow.com/questions/51905191/how-do-i-stop-execution-inside-exec-command-in-python-3