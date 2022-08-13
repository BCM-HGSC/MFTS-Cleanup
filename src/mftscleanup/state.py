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
    if not isinstance(state, State):
        raise TypeError(f"bad state: {state!r}")
    value = state.value
    if value < State.cleanup.value:
        return State(value + 1)
    return None


def get_active_shares(active_dir: Path) -> Iterator[str]:
    """
    Return the names (eg. "rt1234") of all the active shares.
    """
    shares = set()
    for yaml_file_path in active_dir.glob("*.yaml"):
        share_name = yaml_file_path.name.rsplit("_", 1)[0]
        shares.add(share_name)
    return sorted(shares)


def get_share_state(active_dir: Path, share_name: str) -> tuple[State, date]:
    raise NotImplementedError  # TODO
