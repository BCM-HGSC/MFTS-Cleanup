from datetime import date
from enum import Enum
from functools import total_ordering
from pathlib import Path
from typing import Iterator, Optional, Tuple, Union

import yaml

from mftscleanup import business_days

@total_ordering
class OrderingAndIncrementMixin:
    """
    Provides ordering on value. There is an exception that the "hold"
    member must NOT be compared.
    """

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            if "hold" in (self.name, other.name):
                return NotImplemented
            return self.value < other.value
        return NotImplemented

    @property
    def next(self) -> Union["State", None]:
        return get_next_state(self)


State = Enum(
    "State",
    "initial first_email second_email final_email cleanup hold",
    type=OrderingAndIncrementMixin,
)


STATE_NAMES = [s.name for s in State]


def get_transition(
    start_state: State, start_state_date: date
) -> Tuple[Optional[State], Optional[date]]:
    """
    Given a state and associated date, compute the next state and the date of change.

    Return (None, None) if the start state is State.cleanup or State.hold
    """
    #  implement get_next_state and add_business_days to get_transition to pass
    s = State 
    start_state_date = date.fromisoformat(s)
    for s in start_state:
        new_state = s.next()
        new_date = start_state_date.add_business_days
        for date in new_date:
            if start_state in new_state == State.cleanup:
                return (None,None)
            if start_state in new_state  == State.hold:
                return (None,None)

    return new_state, new_date

    return State.first_email, date(2020, 1, 23)  # sample result
    raise NotImplementedError  # TODO


def get_next_state(state: State) -> Union[State, None]:
    """
    initial -> first_email -> second_email -> final_email -> cleanup -> None

    It is an error to call this with anything other than a State.
    Calling with State.cleanup or State.hold should return None.
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


def get_share_state(active_dir: Path, share_id: str) -> tuple[State, date]:
    yaml_file_path = max(active_dir.glob(f"{share_id}_*.yaml"))
    with open(yaml_file_path, "r") as yaml_file:
        try:
            payload = yaml.safe_load(yaml_file)
        except yaml.parser.ParserError as e:
            raise EventFileCorruptError(f"YAML file is corrupt: {yaml_file=}") from e
    if not isinstance(payload, dict):
        raise EventNotDictError(f"YAML file is not a dict: {yaml_file=}")
    if payload["share_id"] != share_id:
        raise InconsistentEventError(
            f"YAML file contents do not match the file name: "
            f"{share_id=} {yaml_file_path=}"
        )
    results = []
    for key, value in payload.items():
        attribute = str(key)
        if attribute.endswith("_date"):
            state_name = attribute.removesuffix("_date")
            if state_name not in STATE_NAMES:
                raise BadStateError(f"bad {state_name=} in {yaml_file_path=}")
            state = State[state_name]
            state_date = date.fromisoformat(value)
            results.append((state, state_date))
    if not results:
        raise MissingStateError(f"no state found in {yaml_file_path}")
    if len(results) > 1:
        raise AmbiguousStateError(f"ambiguous state in {yaml_file_path=}")
    return results[0]


class BadEventFileError(RuntimeError):
    """The YAML file for a share event is bad."""


class EventFileCorruptError(BadEventFileError):
    """File contents are not YAML."""


class EventNotDictError(BadEventFileError):
    """The YAML payload is something other than a dict."""


class InconsistentEventError(BadEventFileError):
    """The YAML payload does not match the file name."""


class BadStateError(BadEventFileError):
    """The YAML payload contains a bad (made-up) state name."""


class MissingStateError(BadEventFileError):
    """The YAML payload contains no state."""


class AmbiguousStateError(BadEventFileError):
    """The YAML payload contains more than one state."""
