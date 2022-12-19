from datetime import date
from enum import Enum
from functools import total_ordering
from typing import Optional, Tuple

from mftscleanup.business_days import add_business_days


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
    def next(self) -> Optional["State"]:
        return get_next_state(self)


State = Enum(
    "State",
    "initial first_email second_email final_email cleanup hold",
    type=OrderingAndIncrementMixin,
)


STATE_NAMES = [s.name for s in State]


def get_transition(
    current_state: State, current_state_start_date: date
) -> Tuple[Optional[State], Optional[date]]:

    if current_state == State.initial:
        number_of_business_days = 15
    elif current_state == State.first_email:
        number_of_business_days = 3
    elif current_state == State.second_email:
        number_of_business_days = 1
    elif current_state == State.final_email:
        number_of_business_days = 1
    elif current_state == State.cleanup:
        return (None, None)
    elif current_state == State.hold:
        return (None, None)

    new_date = add_business_days(current_state_start_date, number_of_business_days)
    new_state = current_state.next

    return new_state, new_date


def get_next_state(state: State) -> Optional[State]:
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
