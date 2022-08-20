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

import argparse
from datetime import date
from os.path import isdir
from pathlib import Path
from sys import argv as sysargv
from sys import stderr
from typing import Optional, Sequence

from addict import Dict
import yaml

from . import __version__
from .cleanup import new_share, process_active_shares
from .email import Emailer


def main(argv: Optional[Sequence[str]] = None):
    """
    Handles being invoked using `python -m mftscleanup ...`
    """
    argv = argv or sysargv[1:]
    if not argv:
        command = "--help"
    else:
        command = argv[0]
        del argv[0]
    if command == "--help":
        print("required: COMMAND CONFIG_FILE ...", file=stderr)
        print("    COMMAND = new | auto", file=stderr)
    elif command == "new":
        return register_new_share(argv)
    elif command == "auto":
        return auto_cleanup_shares(argv)
    else:
        print(f"bad command: {command}. See --help.", file=stderr)


def register_new_share(argv: Optional[Sequence[str]] = None):
    args = parse_register_new_share_command_line(argv)
    new_share(
        args.metadata_root,
        args.sponsor_id,
        args.share_id,
        args.share_directory_path,
        args.email_addresses,
        date.today(),
    )


def parse_register_new_share_command_line(argv: Optional[Sequence[str]] = None):
    """
    `register-new-share CONFIG_FILE_PATH RT_NUMBER SHARE_DIRECTORY_PATH EMAIL [EMAIL]...`
    """
    parser = argparse.ArgumentParser(description="Registering a new share")

    parser.add_argument("metadata_root")
    parser.add_argument("sponsor_id")
    parser.add_argument("rt_number")
    parser.add_argument("share_directory_path", type=dir_path)
    parser.add_argument("email_addresses", nargs="+")
    args = parser.parse_args(argv)

    args.share_id = "rt" + args.rt_number

    print("Registering a new share:")
    for arg in vars(args):
        print("{} is {}".format(arg, getattr(args, arg)))

    return args


def auto_cleanup_shares(argv: Optional[Sequence[str]] = None):
    args = parse_auto_cleanup_shares_command_line(argv)
    metadata_root = args.metadata_root
    email_config = load_config(metadata_root / "email_settings.yaml")
    emailer = Emailer(
        email_config.from_address,
        email_config.host,
    )
    process_active_shares(metadata_root, date.today(), emailer)


def parse_auto_cleanup_shares_command_line(argv: Optional[Sequence[str]] = None):
    """
    `auto-cleanup-shares METADATA_ROOT`
    """
    parser = argparse.ArgumentParser(
        description="Required aguments to run include the following:"
    )
    parser.add_argument("metadata_root", type=dir_path)
    arguments = parser.parse_args(argv)
    return arguments


def dir_path(string):
    if isdir(string):
        return Path(string)
    else:
        raise NotADirectoryError(string)


def load_config(config_file_path):
    with open(config_file_path) as f:
        config = Dict(yaml.safe_load(f))
    return config


if __name__ == "__main__":
    main()
