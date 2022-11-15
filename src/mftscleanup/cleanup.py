"""
Implements the registration and automatic cleanup of shares.
Operates just below command line parsing.
"""


from datetime import date
from logging import getLogger
from pathlib import Path
from os.path import getsize

from .metadata_store import MetadataStore


logger = getLogger(__name__)


def new_share(
    metadata_store: MetadataStore,
    sponsor_id: str,
    share_id: str,
    share_directory: Path,
    email_addresses: list[str],
    start_date: date,
):
    """
    Creates a YAML file that documents the new share.
    """
    assert share_directory.is_dir(), share_directory
    no_of_files, t_file_size = get_directory_totals(share_directory)
    payload = dict(
        sponsor_id=sponsor_id,
        share_id=share_id,
        share_directory=str(share_directory),
        email_addresses=email_addresses,
        initial_date=str(start_date),
        num_files=no_of_files,
        state="initial",
        num_bytes=t_file_size,
    )
    metadata_store.write_event(payload, share_id, "0000")


def get_directory_totals(top: Path):
    num_files = total_size = 0
    for p in list(top.rglob("*")):
        if p.is_file():
            num_files += 1
            total_size += getsize(p)
    return num_files, total_size


def process_active_shares(metadata_store: MetadataStore, effective_date: date):
    assert isinstance(metadata_store, MetadataStore), metadata_store
    for share_id in metadata_store.get_active_shares():
        logger.info(f"processing {share_id}")
        try:
            process_share(metadata_store, share_id, effective_date)
            logger.info(f"finished {share_id}")
        except NotImplementedError as e:
            # raise RuntimeError from e  # Uncomment this line to see the exception.
            raise  # Expected during development (xfail), not production.
        except Exception:
            logger.exception(f"problem with {share_id}")


def process_share(metadata_store: MetadataStore, share_id: str, effective_date: date):
    state, state_date = metadata_store.get_share_state(share_id)
    raise NotImplementedError  # TODO
