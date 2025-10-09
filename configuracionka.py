import os, shlex

while True:
    username = os.getenv('USER', 'user')
    hostname = os.uname().nodename if hasattr(os, 'uname') else 'localhost'
    a = input(f"{username}@{hostname}:~$ ")
    if a.strip() == 'exit':
        break
    if not a.strip():
        continue
    try:
        b = [os.path.expandvars(tok) for tok in shlex.split(a)]
    except ValueError as e:
        print(f"parse: {e}")
        continue
    if b[0] in ("ls", "cd"):
        print(" ".join(b))
    else:
        print(f"{b[0]}: команда не найдена")