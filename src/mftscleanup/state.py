from datetime import date
from enum import Enum, auto
from functools import total_ordering

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
    def next(self) -> "State":
        """
        INITIAL -> FIRST_EMAIL -> SECOND_EMAIL -> FINAL_EMAIL -> CLEANUP
        The result for State.CLEANUP or State.HOLD is self.
        """
        value = self.value
        if value < self.__class__.CLEANUP.value:
            return State(value + 1)
        return self


STATE_NAMES = [s.name for s in State]


def get_deletion_date(
    current_state: State, current_state_start_date: date
) -> date | None:
    """
    Return the anticipated deletion date. This should be None if current_state is
    cleanup or hold. This should be 20 business days after state_start_date if
    current_state is initial.
    #"""
    if current_state == State.CLEANUP or current_state == State.HOLD:
        return None
    if current_state == State.INITIAL:
        num_business_days = 20
    elif current_state == State.FIRST_EMAIL:
        num_business_days = 5
    elif current_state == State.SECOND_EMAIL:
        num_business_days = 2
    elif current_state == State.FINAL_EMAIL:
        num_business_days = 1
    else:
        assert False, (current_state, current_state_start_date)
    deletion_date = add_business_days(current_state_start_date, num_business_days)
    return deletion_date


def get_transition(
    current_state: State, current_state_start_date: date
) -> tuple[State, date | None]:
    """
    Return the next state and the date of transition to that new state. Return
    None for date if the next state is the current state.
    """
    if current_state in (State.CLEANUP, State.HOLD):
        return current_state, None

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
    assert new_state is not None, (current_state, current_state_start_date)

    return new_state, new_date
