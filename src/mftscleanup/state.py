from datetime import date
from enum import Enum, auto
from functools import total_ordering
from typing import Optional

from mftscleanup.business_days import add_business_days


@total_ordering
class State(Enum):
    INITIAL = auto()
    FIRST_EMAIL = auto()
    SECOND_EMAIL = auto()
    FINAL_EMAIL = auto()
    CLEANUP = auto()
    HOLD = auto()

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            if "HOLD" in (self.name, other.name):
                return NotImplemented
            return self.value < other.value
        return NotImplemented

    @property
    def next(self) -> Optional["State"]:
        return get_next_state(self)


STATE_NAMES = [s.name for s in State]


def get_transition(
    current_state: State, current_state_start_date: date
) -> tuple[State | None, date | None]:
    if current_state in (State.CLEANUP, State.HOLD):
        return (None, None)

    if current_state == State.INITIAL:
        number_of_business_days = 15
    elif current_state == State.FIRST_EMAIL:
        number_of_business_days = 3
    elif current_state == State.SECOND_EMAIL:
        number_of_business_days = 1
    elif current_state == State.FINAL_EMAIL:
        number_of_business_days = 1
    else:
        assert False, (current_state, current_state_start_date)

    new_date = add_business_days(current_state_start_date, number_of_business_days)
    new_state = current_state.next

    return new_state, new_date


def get_next_state(state: State) -> State | None:
    """
    initial -> first_email -> second_email -> final_email -> cleanup -> None

    It is an error to call this with anything other than a State.
    Calling with State.CLEANUP or State.HOLD should return None.
    """
    if not isinstance(state, State):
        raise TypeError(f"bad state: {state!r}")
    value = state.value
    if value < State.CLEANUP.value:
        return State(value + 1)
    return None
