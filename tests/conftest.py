from pathlib import Path

from pytest import fixture


@fixture
def directory_skeleton(tmp_path: Path) -> Path:
    root = tmp_path / "metadata_root"
    active = root / "active"
    archive = root / "archive"
    data = tmp_path / "data"
    for p in (root, active, archive, data):
        p.mkdir()
    return tmp_path
