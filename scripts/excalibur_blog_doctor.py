#!/usr/bin/env python3
"""Preflight checks for Excalibur BLOG pipeline."""

from __future__ import annotations

import argparse
import importlib.util
import os
import subprocess
import sys
from pathlib import Path


def project_root() -> Path:
    env_root = os.environ.get("EXCALIBUR_PROJECT_ROOT", "").strip()
    if env_root:
        return Path(env_root)
    return Path(__file__).resolve().parents[1]


def check(condition: bool, label: str, errors: list[str], warnings: list[str], *, warn: bool = False) -> None:
    if condition:
        print(f"OK {label}")
        return
    if warn:
        warnings.append(label)
        print(f"WARN {label}")
    else:
        errors.append(label)
        print(f"FAIL {label}")


def module_available(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def read_env_file(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    if not path.is_file():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            env[key.strip()] = value.strip()
    return env


def merged_publish_env(root: Path) -> dict[str, str]:
    keys = {
        "PUBLIC_SITE_URL",
        "WP_HOME",
        "WP_SITE_URL",
        "FTP_HOST",
        "FTP_PORT",
        "FTP_USER",
        "FTP_PASS",
        "FTP_PASSWORD",
        "FTP_ROOT",
        "FTP_PATH",
        "SSH_HOST",
        "SSH_PORT",
        "SSH_USER",
        "SSH_PASS",
        "SSH_PASSWORD",
        "SSH_ROOT",
        "EXCALIBUR_BLOG_ALLOW_PUBLISH",
    }
    env = read_env_file(root / "memory/site.env.local")
    for key in keys:
        value = os.environ.get(key)
        if value:
            env[key] = value
    if not env.get("FTP_PASS") and env.get("FTP_PASSWORD"):
        env["FTP_PASS"] = env["FTP_PASSWORD"]
    if not env.get("SSH_PASS") and env.get("SSH_PASSWORD"):
        env["SSH_PASS"] = env["SSH_PASSWORD"]
    return env


def git_ls_files(root: Path, pathspec: str) -> list[str]:
    proc = subprocess.run(
        ["git", "ls-files", pathspec],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description="Excalibur BLOG preflight doctor")
    parser.add_argument("--publish", action="store_true", help="Require publish credentials and allow flag")
    args = parser.parse_args()

    root = project_root()
    errors: list[str] = []
    warnings: list[str] = []

    print(f"EXCALIBUR_ROOT={root}")

    check((root / "AGENTS.md").is_file(), "AGENTS.md exists", errors, warnings)
    check((root / ".cursor-plugin/plugin.json").is_file(), ".cursor-plugin/plugin.json exists", errors, warnings)
    check((root / ".cursor/agents").is_dir(), ".cursor/agents exists", errors, warnings)
    check((root / ".cursor/skills").is_dir(), ".cursor/skills exists", errors, warnings)
    check((root / "shared/excalibur-blog-handoff.template.md").is_file(), "handoff template exists", errors, warnings)
    check(
        not git_ls_files(root, "shared/excalibur-blog-handoff.md"),
        "runtime shared/excalibur-blog-handoff.md is not tracked",
        errors,
        warnings,
    )
    check(
        ".cursor/excalibur-blog-handoff.md" in (root / ".gitignore").read_text(encoding="utf-8"),
        ".cursor handoff ignored",
        errors,
        warnings,
    )

    check(module_available("PIL"), "Pillow available", errors, warnings)
    check(module_available("numpy"), "numpy available", errors, warnings)

    interlinker = root / "scripts/excalibur_blog_interlinker.py"
    help_proc = subprocess.run(
        [sys.executable, str(interlinker), "--help"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    check("--article-dir" in help_proc.stdout, "interlinker supports --article-dir", errors, warnings)

    llms = root / "scripts/excalibur_blog_llms_generator.py"
    llms_help = subprocess.run(
        [sys.executable, str(llms), "--help"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    check("--blog-path" in llms_help.stdout, "llms generator supports --blog-path", errors, warnings)

    env = merged_publish_env(root)
    has_public = bool(env.get("PUBLIC_SITE_URL") or env.get("WP_HOME") or env.get("WP_SITE_URL"))
    check(has_public, "PUBLIC_SITE_URL/WP_SITE_URL configured", errors, warnings, warn=not args.publish)
    check(bool(env.get("SSH_HOST") or env.get("FTP_HOST")), "SFTP host configured", errors, warnings, warn=not args.publish)
    check(bool(env.get("SSH_USER") or env.get("FTP_USER")), "SFTP user configured", errors, warnings, warn=not args.publish)
    check(
        bool(env.get("SSH_PASS") or env.get("FTP_PASS") or env.get("SSH_PASSWORD") or env.get("FTP_PASSWORD")),
        "SFTP password configured",
        errors,
        warnings,
        warn=not args.publish,
    )
    check(
        env.get("EXCALIBUR_BLOG_ALLOW_PUBLISH", "").strip().lower() == "yes",
        "EXCALIBUR_BLOG_ALLOW_PUBLISH=yes",
        errors,
        warnings,
        warn=not args.publish,
    )

    print(f"SUMMARY errors={len(errors)} warnings={len(warnings)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
