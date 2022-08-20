"""
Implements the registration and automatic cleanup of shares.
Operates just below command line parsing.
"""


from datetime import date
from logging import getLogger
from pathlib import Path
from os.path import getsize
from typing import Union

from yaml import dump

from .email import Emailer
from .state import get_active_shares, get_share_state


logger = getLogger(__name__)


def new_share(
    metadata_root: Union[str, Path],
    share_id: str,
    share_directory: Path,
    email_addresses,
    start_date: date,
):
    """
    Creates a YAML file that documents the new share.
    """
    assert share_directory.is_dir(), share_directory
    no_of_files, t_file_size = get_directory_totals(share_directory)
    payload = dict(
        share_id=share_id,
        share_directory=str(share_directory),
        email_addresses=email_addresses,
        initial_date=str(start_date),
        num_files=no_of_files,
        state="initial",
        num_bytes=t_file_size,
    )
    destination = Path(metadata_root) / "active" / f"{share_id}_0000.yaml"
    directory = destination.parent
    directory.mkdir(parents=True, exist_ok=True)
    destination.write_text(dump(payload), encoding="UTF-8")


def get_directory_totals(top: Path):
    num_files = total_size = 0
    for p in list(top.rglob("*")):
        if p.is_file():
            num_files += 1
            total_size += getsize(p)
    return num_files, total_size


def process_active_shares(metadata_root: Path, effective_date: date, emailer: Emailer):
    assert isinstance(metadata_root, Path), metadata_root
    for share_id in get_active_shares(metadata_root / "active"):
        logger.info(f"processing {share_id}")
        try:
            process_share(metadata_root, share_id, effective_date, emailer)
            logger.info(f"finished {share_id}")
        except Exception:
            logger.exception(f"problem with {share_id}")


def process_share(
    metadata_root: Path, share_id: str, effective_date: date, emailer: Emailer
):
    state, state_date = get_share_state(metadata_root / "active", share_id)
    raise NotImplementedError  # TODO
