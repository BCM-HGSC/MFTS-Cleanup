"""
Implements the registration and automatic cleanup of shares.
Operates just below command line parsing.
"""

from os import access
import pathlib
from yaml import dump

def new_share(metadata_root, rt_number, share_directory, email_addresses, no_of_files, t_file_size):
    """
    Creates a YAML file that documents the new share.
    """
    payload = dict(
        rt_number = int(rt_number),
        share_directory = str(share_directory),
        email_addresses = email_addresses,
        number_of_files = no_of_files,
        total_file_size = t_file_size


    )
    destination = pathlib.Path(metadata_root) / "active" / f"{rt_number}_initial.yaml"
    directory = destination.parent
    directory.mkdir(parents=True, exist_ok=True)
    destination.write_text(dump(payload), encoding="UTF-8")  
   

def new_cleanup(config_file_path):
    active_dir = config_file_path.parent
    top = pathlib.Path(active_dir)
    for p in top.rglob("*"):
        if p.is_file():
            print(p)

 



        
    pass
    # payload = dict(
    # #     rt_number = int(rt_number)
    # )
    # destination = Path(metadata_root) / "active" / f"{rt_number}_first_email.yaml"
    # directory = destination.parent
    # directory.mkdir(parents=True, exist_ok=True)
    # destination.write_text(dump(payload), encoding="UTF-8")  

    