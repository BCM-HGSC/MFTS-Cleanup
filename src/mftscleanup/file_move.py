# from msilib.schema import Directory
from datetime import datetime
from .send_email import obtain_dir
import shutil
from pathlib import Path
# print(dir(shutil))

# src = (/Users/u242806/MFTS-Cleanup/test/path)
# dest = (/test/aspera/mfts/rharris/rt1234)

# shutil.copyfile(src,dest)


def move_dirs(obtain_dir):
    obtain_dir = obtain_dir(Path)
    shutil.copyfile(obtain_dir,'test/path')


def check_for_update(directory):
    # get time as string
    now = datetime.now()
    
    # bringing directory from send_email
    file_dir = obtain_dir(Path)
    print(file_dir)

