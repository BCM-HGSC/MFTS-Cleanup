"""
Implements the registration and automatic cleanup of shares.
Operates just below command line parsing.
"""


from datetime import date, timedelta
import pathlib
from os.path import getsize

from addict import Dict
from yaml import dump, safe_load


def new_share(
    metadata_root,
    rt_number,
    share_directory: pathlib.Path,
    email_addresses,
    start_date=None,
):
    """
    Creates a YAML file that documents the new share.
    """
    if start_date is None:
        start_date = date.today()
    assert share_directory.is_dir(), share_directory
    no_of_files, t_file_size = get_directory_totals(share_directory)
    payload = dict(
        rt_number=int(rt_number),
        share_directory=str(share_directory),
        email_addresses=email_addresses,
        number_of_files=no_of_files,
        total_file_size=t_file_size,
        registration_date=str(start_date),
    )
    destination = pathlib.Path(metadata_root) / "active" / f"{rt_number}_initial.yaml"
    directory = destination.parent
    directory.mkdir(parents=True, exist_ok=True)
    destination.write_text(dump(payload), encoding="UTF-8")


def get_directory_totals(top: pathlib.Path):
    num_files = total_size = 0
    for p in list(top.rglob("*")):
        if p.is_file():
            num_files += 1
            total_size += getsize(p)
    return num_files, total_size


def process_active_shares(metadata_root, from_address, email_host):
    active_dir = pathlib.Path(metadata_root) / "active"
    today = date.today()
    for p in active_dir.rglob("*_initial.yaml"):
        if p.is_file():
            with open(p) as f:
                rt_share_info = Dict(safe_load(f))
            process_share(rt_share_info, today)


def process_share(rt_share_info, today):
    print(rt_share_info)
    registration_date = date.fromisoformat(rt_share_info.registration_date)
    print(repr(registration_date), repr(today))

    if (today) - (registration_date) < timedelta(21):
        print("not enough time")
    elif (today) - (registration_date) == timedelta(21):
        print("yaml_file1")
    elif (today) - (registration_date) == timedelta(25):
        print("yaml_file2")
    elif (today) - (registration_date) == timedelta(27):
        print("yaml_file3")
    else:
        print("no action required")
