from pykeepass import PyKeePass
import os
from typing import TextIO

def get_password(kp_entry: str, kdbx_path: TextIO, db_pass_env: str):
    Password = os.getenv(db_pass_env) 
    kp = PyKeePass(kdbx_path, password=Password)
    for entry in kp.entries:
        if entry.title == kp_entry:
           # print(entry.password)
            return entry.password
        else:
            continue
        
if __name__ == '__main__':
    kp_entry = 'Dev Env API token'
    kdbx_path = r"C:\Users\zieloma4\OneDrive - orange.com\Pulpit\Work.kdbx"
    db_pass_env = "KeePassKey"
  #  entry_pass_env = "GITLAB_ACCESS_TOKEN"
    get_password(kp_entry, kdbx_path, db_pass_env)
    
    