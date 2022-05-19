"""
By naming the top-level module __main__, it is possible to run this module as
a script by running:
`python -m mftscleanup [args...]`
"""

import argparse,os
from ast import arguments

from os.path import getsize
from pathlib import Path
from sys import argv
from textwrap import dedent

from addict import Dict
import yaml

from . import __version__
from .cleanup import new_share


def main():
    print(
        dedent(
            f"""\
            {__package__=} (v{__version__})
            {__name__=} @ {__file__}

            {argv=}
            """  # This f-string syntax requires 3.8+
        )
    )
    print("this is a test")
    # for p in path:
    #     print(p)

def get_directory_totals(directory_path):
    top= Path(directory_path)
    num_files = total_size = 0
    for p in list(top.rglob("*")):
        if p.is_file():
            num_files += 1
            total_size += getsize(p)
    return num_files, total_size


def register_share():
    args = parse_register_command_line()
    config = load_config(args.config_file_path)
    # f_num_size = get_directory_totals(".")
    no_of_files = get_directory_totals(".")[0]
    t_file_size = get_directory_totals(".")[1]

    new_share(
        config.metadata_root, args.rt_number, args.share_directory_path, args.email_addresses, 
        no_of_files, t_file_size
        )


def parse_register_command_line():
    """
    `register-new-share CONFIG_FILE_PATH RT_NUMBER SHARE_DIRECTORY_PATH EMAIL [EMAIL]...`
    """
    parser= argparse.ArgumentParser(description="Registering a new share")

    parser.add_argument('config_file_path')
    parser.add_argument('rt_number')
    parser.add_argument('share_directory_path', type= dir_path)
    parser.add_argument('email_addresses', nargs="+")
    args = parser.parse_args()

    print("Registering a new share:")
    for arg in vars(args):
        print("{} is {}".format(arg, getattr(args, arg)))

    return args


def dir_path(string):
    if os.path.isdir(string):
        return Path(string)
    else:
        raise NotADirectoryError(string)


def load_config(config_file_path):
    with open(config_file_path) as f:
        config = Dict(yaml.safe_load(f))
    return config



"""
this is where auto_cleanup functions begin

"""

def auto_cleanup():
    arguments = start_cleanup()
    config = load_config(arguments.config_file_path)

    new_share(
        config.metadata_root, arguments.rt_number
        )


def start_cleanup():
    print("Hello World")
    """
    `auto-cleanup-shares CONFIG_FILE_PATH `
    """
    parser = argparse.ArgumentParser(description= "Required aguments to run include the following:")
    parser.add_argument('config_file_path')
    parser.add_argument('rt_number', type=int)
    arguments = parser.parse_args()
    print("Obtaining config file")

    return arguments
    


 

def process_cleanup():
    pass
    # args = start_cleanup()
    # config = load_config(args.config_file_path)
    


    # start_cleanup(
    #     config.auto_cleanup
    # )


if __name__ == "__main__":
    main()
