"""
This is the CLI interface. This module is responsible for just:

- parsing the config file
- parsing the command line
- configuring logging

Application logic starts in cleanup.py.

There are 4 ways to run the code here:

1. Use one of the console_scripts defined in setup.cfg.
2. `python -m mftscleanup [args...]`
3. `python path/to/code/src [args...]`
4. `python path/to/code/src/mftscleanup [args...]`

Since there are more than one console_scripts, calling this module directly
requires specify which command is intended.
"""

import argparse, os

from pathlib import Path
from sys import argv, stderr

from addict import Dict
import yaml

from . import __version__
from .cleanup import new_share, process_active_shares


def main():
    if len(argv) < 2:
        command = "--help"
    else:
        command = argv[1]
        del argv[1]
    if command == "--help":
        print("required: COMMAND CONFIG_FILE ...", file=stderr)
        print("    COMMAND = new | auto", file=stderr)
    elif command == "new":
        return register_share()
    elif command == "auto":
        return auto_cleanup()
    else:
        print(f"bad command: {command}. See --help.", file=stderr)


def register_share():
    args = parse_register_command_line()
    config = load_config(args.config_file_path)
    new_share(
        config.metadata_root,
        args.share_id,
        args.share_directory_path,
        args.email_addresses,
    )


def parse_register_command_line():
    """
    `register-new-share CONFIG_FILE_PATH RT_NUMBER SHARE_DIRECTORY_PATH EMAIL [EMAIL]...`
    """
    parser = argparse.ArgumentParser(description="Registering a new share")

    parser.add_argument("config_file_path")
    parser.add_argument("rt_number")
    parser.add_argument("share_directory_path", type=dir_path)
    parser.add_argument("email_addresses", nargs="+")
    args = parser.parse_args()

    args.share_id = "rt" + args.rt_number

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
Implements the cleanup of directories

"""


def auto_cleanup():
    args = start_cleanup()
    config = load_config(args.config_file_path)

    process_active_shares(
        config.metadata_root,
        config.email.from_address,
        config.email.host,
    )


def start_cleanup():
    """
    `auto-cleanup-shares CONFIG_FILE_PATH `
    """
    parser = argparse.ArgumentParser(
        description="Required aguments to run include the following:"
    )
    parser.add_argument("config_file_path", type=Path)
    arguments = parser.parse_args()
    return arguments


if __name__ == "__main__":
    main()
