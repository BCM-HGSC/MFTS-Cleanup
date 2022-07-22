from datetime import date
from enum import Enum
from pathlib import Path
from typing import Iterator, Union


State = Enum("State", "initial first_email second_email final_email cleanup")


def get_next_state(state: State) -> Union[State, None]:
    """
    initial -> first_email -> second_email -> final_email -> cleanup -> None

    It is an error to call this with anything other than a State.
    Calling with State.cleanup should return None.
    """
    raise NotImplementedError  # TODO


def get_active_shares(active_dir: Path) -> Iterator[str]:
    """
    Return the names (eg. "rt1234") of all the active shares.
    """
    raise NotImplementedError  # TODO


def get_share_state(active_dir: Path, share_name: str) -> tuple[State, date]:
    raise NotImplementedError  # TODO
