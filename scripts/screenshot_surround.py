"""Find the flat border around a device screenshot, and the operators that remove it.

A device screenshot exported onto a flat backdrop arrives with a border of that
one color around the device. Both image scripts use this module: the AVIF
converter so the site shows the device on the page background, and the App
Store script so the canvas margin meets the device rather than a box around it.

The border is cleared inward from the four corners and the image cropped to the
device. A bare screenshot whose own background reaches the corners is told
apart by what clearing leaves: one solid device for a border, scattered pieces
of content for an app's background.
"""

from __future__ import annotations

import math
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


PIXEL_NUMBER = re.compile(r"\d+(?:\.\d+)?")

# Clearing a backdrop from the corners leaves the device as one solid region,
# give or take a speck of capture debris, and also takes the bits of backdrop
# beside its rounded corners and buttons, a few percent of its bounding box.
# Clearing an app's own background, where a bare screenshot's reaches its
# corners, leaves its content in pieces instead, and that screenshot is left
# alone.
MIN_DEVICE_SHARE = 0.99
MAX_CLEARED_INSIDE = 0.10

# A line of ImageMagick's connected-components listing:
# "  1: 1243x1622+15+10 633.8,822.3 1.99777e+06 srgb(255,255,255)".
REGION_LINE = re.compile(r"\s*\d+: (\d+)x(\d+)\+(\d+)\+(\d+) \S+ (\S+) (\S+)")


@dataclass(frozen=True)
class Surround:
    """A flat-colored border around the device, and the size of what it surrounds."""

    arguments: list[str]
    width: int
    height: int


def probe_corners(magick: str, path: Path) -> tuple[int, int, list[tuple[float, ...]]]:
    """Return the size and the four corner pixels in one ImageMagick call."""
    result = subprocess.run(
        [
            magick,
            str(path),
            "-depth",
            "8",
            "-format",
            "%w %h|%[pixel:p{0,0}]|%[pixel:p{%[fx:w-1],0}]"
            "|%[pixel:p{0,%[fx:h-1]}]|%[pixel:p{%[fx:w-1],%[fx:h-1]}]",
            "info:",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    size_field, *corner_fields = result.stdout.strip().split("|")
    width, height = (int(value) for value in size_field.split())
    corners = [corner_channels(field) for field in corner_fields]
    return width, height, corners


def corner_channels(field: str) -> tuple[float, ...]:
    """Red, green, blue, and alpha if any, from a pixel ImageMagick printed.

    A grayscale image prints gray(255) or graya(255,0.5), one value standing for
    all three channels, so it is spread across them.
    """
    numbers = tuple(float(number) for number in PIXEL_NUMBER.findall(field))
    if field.startswith("gray"):
        return numbers[:1] * 3 + numbers[1:]
    return numbers


def color_distance(first: tuple[float, ...], second: tuple[float, ...]) -> float:
    """Distance between two 0-255 colors, as a percentage, the way -fuzz reads it."""
    squares = sum((a - b) ** 2 for a, b in zip(first[:3], second[:3]))
    return math.sqrt(squares / 3) / 255 * 100


def find_surround(magick: str, path: Path, fuzz: int) -> Surround | None:
    """The flat border around a device screenshot, or None when there is none.

    It counts only when all four corners are opaque and one color, and clearing
    it from the corners leaves one solid region holding nearly everything left,
    with a margin on every side and little of its bounding box cleared. The
    crop goes to that region, so a speck of debris at the edge goes with the
    border.
    """
    width, height, corners = probe_corners(magick, path)
    for corner in corners:
        # ImageMagick reports color channels as 0-255 but alpha as 0-1.
        alpha = corner[3] if len(corner) > 3 else 1.0
        if len(corner) < 3 or alpha < 0.99:
            return None
    if any(color_distance(corner, corners[0]) > fuzz for corner in corners[1:]):
        return None

    clearing = ["-alpha", "set", "-fuzz", f"{fuzz}%", "-fill", "none"]
    points = ((0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1))
    for (x, y), corner in zip(points, corners):
        red, green, blue = (round(channel) for channel in corner[:3])
        clearing.extend(["-floodfill", f"+{x}+{y}", f"rgb({red},{green},{blue})"])

    result = subprocess.run(
        [
            magick,
            str(path),
            *clearing,
            "-alpha",
            "extract",
            "-threshold",
            "50%",
            "-define",
            "connected-components:verbose=true",
            "-connected-components",
            "8",
            "null:",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    # Solid regions are white in the extracted alpha, cleared ones black.
    solid = [
        (float(match[5]), int(match[1]), int(match[2]), int(match[3]), int(match[4]))
        for match in map(REGION_LINE.match, result.stdout.splitlines())
        if match and "255" in match[6]
    ]
    if not solid:
        return None

    area, inner_width, inner_height, left, top = max(solid)
    margins = (left, top, width - left - inner_width, height - top - inner_height)
    cleared = 1 - area / (inner_width * inner_height)
    share = area / sum(region[0] for region in solid)
    if min(margins) < 1 or cleared > MAX_CLEARED_INSIDE or share < MIN_DEVICE_SHARE:
        return None

    crop = ["-crop", f"{inner_width}x{inner_height}+{left}+{top}", "+repage"]
    return Surround([*clearing, *crop], inner_width, inner_height)
