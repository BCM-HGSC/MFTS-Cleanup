"""
By naming the top-level module __main__, it is possible to run this module as
a script by running:
`python -m mftscleanup [args...]`
"""

import argparse,os
from pathlib import Path
from sys import argv
from textwrap import dedent

from addict import Dict
import yaml

from . import __version__
from .cleanup import auto_cleanup, new_share


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
    # TODO: check and clean directories
    # TODO: run obtain directory from main
    # TODO: ask for user input on email, rt# , and recipient email
    print("this is a test")
    # for p in path:
    #     print(p)


def register_share():
    args = parse_register_command_line()
    config = load_config(args.config_file_path)
    print(args)
    print(config)
    new_share(
        config.metadata_root, args.rt_number, args.share_directory, args.email_addresses
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

    print("the inputs are:")
    for arg in vars(args):
        print("{} is {}".format(arg, getattr(args, arg)))

    return args
    # return Dict()


def load_config(config_file_path):
    with open(config_file_path, mode= "r") as config_file:
        data = yaml.load(config_file)
    return Dict(data)
    # return Dict(yaml.load(config_file_path))


def dir_path(string):
    if os.path.isdir(string):
        return Path(string)
    else:
        raise NotADirectoryError(string)


if __name__ == "__main__":
    main()
