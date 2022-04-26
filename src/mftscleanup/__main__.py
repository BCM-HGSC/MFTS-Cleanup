"""
By naming the top-level module __main__, it is possible to run this module as
a script by running:
`python -m mftscleanup [args...]`
"""

from sys import argv, path
from textwrap import dedent

from addict import Dict

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
    pass  # TODO
    return Dict()


def load_config(config_file_path):
    pass  # TODO
    return Dict()


if __name__ == "__main__":
    main()
