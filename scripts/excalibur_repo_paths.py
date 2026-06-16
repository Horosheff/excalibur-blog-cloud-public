"""Repo-relative paths for JSON reports (no local usernames in git)."""

from __future__ import annotations

from pathlib import Path


def project_root_from(anchor: Path) -> Path:
    return anchor.resolve().parents[1]


def repo_relative(path: Path, root: Path | None = None) -> str:
    p = path.resolve()
    base = (root or project_root_from(Path(__file__))).resolve()
    try:
        return p.relative_to(base).as_posix()
    except ValueError:
        return p.as_posix()
