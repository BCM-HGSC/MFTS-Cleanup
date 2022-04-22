# from msilib.schema import Directory
import shutil
from datetime import datetime
import send_email as se


# print(dir(shutil))

# src = (/Users/u242806/MFTS-Cleanup/test/path)
# dest = (/test/aspera/mfts/rharris/rt1234)

# shutil.copyfile(src,dest)


def move_dirs(file_dir):
    shutil.copy(file_dir,'')
    shutil.copy(file_dir,'/Users/u242806/BaylorCollegeOfMedicine/repos/mfts_auto/auto_email/')
    os.rename(file_dir, '/test/path')


def check_for_update():
    # get time as string
    now = datetime.now()
    file_dir = obtain_dir.send_email



