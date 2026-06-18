#!/usr/bin/env python3
"""Generate App Store-ready screenshots from source images.

The script scans product folders under source/ for screenshot images, resizes
each screenshot down to the nearest accepted App Store canvas, then centers it
on that canvas. macOS screenshots keep transparent margins. iPhone and iPad
screenshots use white margins because App Store Connect rejects transparency.
"""

from __future__ import annotations

import argparse
import math
import shutil
import subprocess
import sys
from pathlib import Path


APP_STORE_SIZES = {
    "macos": [(1280, 800), (1440, 900), (2560, 1600), (2880, 1800)],
    "iphone": [(1242, 2688), (2688, 1242), (1284, 2778), (2778, 1284)],
    "ipad": [(2064, 2752), (2752, 2064), (2048, 2732), (2732, 2048)],
}

IMAGE_EXTENSIONS = {".avif", ".heic", ".jpg", ".jpeg", ".png", ".tif", ".tiff"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate App Store-ready PNG screenshots with appropriate margins."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("source"),
        help="Directory to scan for source screenshots. Defaults to source/.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("app-store-screenshots"),
        help="Directory for generated PNG screenshots. Defaults to app-store-screenshots/.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove the output directory before generating screenshots.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned outputs without writing files.",
    )
    return parser.parse_args()


def require_magick() -> str:
    magick = shutil.which("magick")
    if not magick:
        print("error: ImageMagick is required; install it so `magick` is on PATH.", file=sys.stderr)
        sys.exit(1)
    return magick


def screenshot_sources(input_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in input_dir.glob("*/*")
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def platform_from_path(path: Path) -> str:
    searchable_name = " ".join(part.lower() for part in path.parts)
    if "iphone" in searchable_name:
        return "iphone"
    if "ipad" in searchable_name:
        return "ipad"
    if "macos" in searchable_name:
        return "macos"
    return "macos"


def image_size(magick: str, path: Path) -> tuple[int, int]:
    result = subprocess.run(
        [magick, "identify", "-format", "%w %h", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    width, height = result.stdout.strip().split()
    return int(width), int(height)


def orientation_matches(width: int, height: int, target_width: int, target_height: int) -> bool:
    if width == height:
        return True
    return (width > height) == (target_width > target_height)


def choose_target(platform: str, width: int, height: int) -> tuple[int, int]:
    candidates = [
        size
        for size in APP_STORE_SIZES[platform]
        if platform == "macos" or orientation_matches(width, height, *size)
    ]

    # Prefer canvases that require the source image to shrink in at least one
    # dimension. This keeps "nearest" from choosing a larger canvas just because
    # the screenshot is a little under an accepted size.
    downscale_candidates = [
        (target_width, target_height)
        for target_width, target_height in candidates
        if target_width <= width or target_height <= height
    ]
    if downscale_candidates:
        candidates = downscale_candidates

    def score(size: tuple[int, int]) -> tuple[float, float]:
        target_width, target_height = size
        distance = math.hypot(target_width - width, target_height - height)
        aspect_penalty = abs((target_width / target_height) - (width / height)) * 1000
        return distance + aspect_penalty, distance

    return min(candidates, key=score)


def output_path(output_dir: Path, source: Path, target: tuple[int, int]) -> Path:
    product_folder = source.parent.name
    target_width, target_height = target
    return output_dir / product_folder / f"{source.stem}-appstore-{target_width}x{target_height}.png"


def convert_screenshot(magick: str, source: Path, output: Path, platform: str, target: tuple[int, int]) -> None:
    target_width, target_height = target
    background = "white" if platform in {"iphone", "ipad"} else "none"
    output.parent.mkdir(parents=True, exist_ok=True)

    command = [
        magick,
        str(source),
        "-alpha",
        "set",
        "-resize",
        f"{target_width}x{target_height}>",
        "-background",
        background,
        "-gravity",
        "center",
        "-extent",
        f"{target_width}x{target_height}",
    ]

    if platform in {"iphone", "ipad"}:
        command.extend(["-alpha", "remove", "-alpha", "off"])

    command.append(str(output))
    subprocess.run(command, check=True)


def main() -> int:
    args = parse_args()
    magick = require_magick()
    input_dir = args.input
    output_dir = args.output

    if not input_dir.exists():
        print(f"error: input directory does not exist: {input_dir}", file=sys.stderr)
        return 1

    sources = screenshot_sources(input_dir)
    if not sources:
        print(f"No screenshot images found under {input_dir}")
        return 0

    if args.clean and output_dir.exists() and not args.dry_run:
        shutil.rmtree(output_dir)

    for source in sources:
        platform = platform_from_path(source)
        width, height = image_size(magick, source)
        target = choose_target(platform, width, height)
        output = output_path(output_dir, source, target)
        background = "white" if platform in {"iphone", "ipad"} else "transparent"
        print(
            f"{source} -> {output} "
            f"({platform}, {width}x{height} -> {target[0]}x{target[1]}, {background})"
        )
        if not args.dry_run:
            convert_screenshot(magick, source, output, platform, target)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
