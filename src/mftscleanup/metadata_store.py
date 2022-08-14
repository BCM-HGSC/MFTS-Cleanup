"""
Stores metadata about shares on the filesystem.
"""

from logging import getLogger
from pathlib import Path
from typing import Union

from addict import Dict
from yaml import safe_dump, safe_load

from .email import Emailer
from .state import State


logger = getLogger(__name__)


class MetadataStore:
    """
    Wraps the top-level directory, which contains the active shares, the archive,
    email configuration, and the mapping file from sponsor ID to sponsor email.
    """

    def __init__(self, metadata_root: Union[str, Path]) -> None:
        self.metadata_root = Path(metadata_root)
        self._active = self.metadata_root / "active"
        self._archive = self.metadata_root / "archive"

    @property
    def active(self) -> Path:
        if not self._active.is_dir():
            self._active.mkdir(parents=True, exist_ok=True)
        return self._active

    @property
    def archive(self) -> Path:
        if not self._archive.is_dir():
            self._archive.mkdir(parents=True, exist_ok=True)
        return self._archive

    def load_emailer(self, emailer_factory=Emailer) -> Emailer:
        email_config = load_config(self.metadata_root / "email_settings.yaml")
        emailer = emailer_factory(
            email_config.from_address,
            email_config.host,
        )
        return emailer

    def get_sponsor_email(self, sponsor_id) -> str:
        raise NotImplementedError  # TODO

    def write_event(self, payload: dict, share_id: str, event_id: str) -> None:
        destination = self.active / f"{share_id}_{event_id}.yaml"
        write_yaml(payload, destination)


def write_yaml(payload: dict, destination: Path) -> None:
    if destination.is_file():
        logger.warning(f"overwriting {destination}")
    directory = destination.parent
    directory.mkdir(parents=True, exist_ok=True)
    yaml_text = safe_dump(payload, default_flow_style=False)
    destination.write_text(yaml_text, encoding="UTF-8")
    logger.info(f"wrote {destination}")


def load_config(config_file_path):
    with open(config_file_path) as f:
        config = Dict(safe_load(f))
    return config
