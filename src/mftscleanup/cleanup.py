"""
Implements the registration and automatic cleanup of shares.
Operates just below command line parsing.
"""


from datetime import date
from logging import getLogger
from pathlib import Path
from os.path import getsize

from .metadata_store import MetadataStore, Share
from .state import get_deletion_date, get_transition, State, STATE_NAMES


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


def process_active_shares(
    metadata_store: MetadataStore, effective_date: date, brittle=False
):
    assert isinstance(metadata_store, MetadataStore), metadata_store
    for share_id in metadata_store.get_active_shares():
        logger.info(f"processing {share_id}")
        try:
            share = metadata_store.load_share(share_id)
            process_share(metadata_store, share, effective_date)
            logger.info(f"finished {share_id}")
        except Exception:
            logger.exception(f"problem with {share_id}")
            if brittle:
                raise


def process_share(metadata_store: MetadataStore, share: Share, effective_date: date):
    start_state, start_state_date = share.state, share.state_date
    new_state, transition_date = get_transition(
        start_state, start_state_date
    )  # TODO: propagate date
    # TODO: handle hold state
    if new_state is None:
        return
    assert transition_date is not None, share.share_id
    if effective_date < transition_date:
        return
    enter_state(metadata_store, share, new_state, effective_date)


def enter_state(
    metadata_store: MetadataStore, share: Share, new_state: State, effective_date: date
) -> None:
    take_state_action(metadata_store, share, new_state, effective_date)
    record_new_state(metadata_store, share.share_id, new_state, effective_date)


def take_state_action(
    metadata_store: MetadataStore, share: Share, new_state: State, effective_date: date
) -> None:
    assert new_state != State.INITIAL, share.share_id
    assert new_state != State.HOLD, share.share_id
    assert new_state.name in STATE_NAMES, (share.share_id, new_state)
    match new_state:
        case State.FIRST_EMAIL:
            send_email(metadata_store, share, new_state, effective_date)
        case State.SECOND_EMAIL:
            send_email(metadata_store, share, new_state, effective_date)
        case State.FINAL_EMAIL:
            send_email(metadata_store, share, new_state, effective_date)
        case State.CLEANUP:
            cleanup_storage(metadata_store, share)
        case _:
            raise AssertionError(f"{share.share_id=} {new_state=}")


def send_email(
    metadata_store: MetadataStore, share: Share, new_state: State, effective_date: date
) -> None:
    recipients = share.email_addresses
    subject, body = construct_email(share, new_state, effective_date)
    assert metadata_store.emailer is not None, share.share_id
    metadata_store.emailer.send_message(recipients, subject, body)


def construct_email(
    share: Share, new_state: State, effective_date: date
) -> tuple[str, str]:
    """
    Return subject and body as pair of strings.
    """
    deletion_date = get_deletion_date(new_state, effective_date)
    subject = (
        f"Scheduled deletion for data from RT #{share.share_id} on {deletion_date}"
        f" at {share.share_directory}"
    )
    raise NotImplementedError  # TODO


def cleanup_storage(metadata_store: MetadataStore, share: Share) -> None:
    raise NotImplementedError  # TODO


def record_new_state(
    metadata_store: MetadataStore, share_id: str, new_state: State, effective_date: date
) -> None:
    """
    Record the new state in a YAML file
    """
    raise NotImplementedError  # TODO
