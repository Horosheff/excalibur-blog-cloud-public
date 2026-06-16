#!/usr/bin/env python3
"""Image signature sniffing and Pillow decode validation for Excalibur BLOG."""
from __future__ import annotations

import io
from pathlib import Path


def sniff_image_format(data: bytes) -> str:
    stripped = data.lstrip()
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if data.startswith(b"\xff\xd8\xff"):
        return "jpeg"
    if data.startswith((b"GIF87a", b"GIF89a")):
        return "gif"
    if len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp"
    if stripped[:128].lower().startswith((b"<svg", b"<?xml")) and b"<svg" in stripped[:512].lower():
        return "svg"
    return ""


def validate_image_file(path: Path) -> list[str]:
    errors: list[str] = []
    suffix = path.suffix.lower().lstrip(".")
    if suffix == "jpg":
        suffix = "jpeg"

    try:
        data = path.read_bytes()
    except OSError as exc:
        return [f"cannot read image asset {path}: {exc}"]

    if not data:
        return [f"empty image asset: {path}"]

    detected = sniff_image_format(data)
    if not detected:
        return [f"image asset has unknown/corrupt signature: {path}"]
    if suffix and suffix != detected:
        errors.append(f"image extension/content mismatch: {path} is .{suffix} but bytes are {detected}")

    if detected == "svg":
        return errors

    try:
        from PIL import Image

        with Image.open(io.BytesIO(data)) as image:
            image.verify()
        with Image.open(io.BytesIO(data)) as image:
            image.load()
    except ImportError:
        errors.append(f"Pillow is not installed; cannot decode-verify raster image: {path}")
    except Exception as exc:  # noqa: BLE001
        errors.append(f"image asset is not decodable by Pillow: {path}: {exc}")

    return errors
