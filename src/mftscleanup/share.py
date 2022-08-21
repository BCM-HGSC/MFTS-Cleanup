"""
Encapsulates the concept of a single share with all its history.

Logic only. No serialization or I/O.
"""

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Optional

from .state import State


@dataclass
class HoldDetails:
    next_state: State
    expiration_date: date


@dataclass(order=True)
class Share:
    share_id: str
    sponsor_id: str
    share_directory: Path
    num_files: int
    num_bytes: int
    email_addresses: list[str]
    state_date: date
    state: State = State.INITIAL
    initial_date: Optional[date] = None
    first_email_date: Optional[date] = None
    second_email_date: Optional[date] = None
    final_email_date: Optional[date] = None
    cleanup_date: Optional[date] = None
    hold_details: Optional[HoldDetails] = None

    def __str__(self):
        return f"Share<{self.share_id}>"

    def assert_valid(self):
        assert self.share_id, self
        assert self.sponsor_id, self
        assert self.share_directory, self
        assert isinstance(self.num_files, int), self
        assert isinstance(self.num_bytes, int), self
        assert self.state, self
        assert self.state_date, self
        # TODO: Validate existence of dates is consistent with state.
        # TODO: Validate ordering relationships between dates.

    def get_sponsor_email(self) -> str:
        raise NotImplementedError  # TODO
