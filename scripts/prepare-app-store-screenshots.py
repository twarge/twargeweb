#!/usr/bin/env python3
"""Generate App Store-ready screenshots from source images.

The script scans product folders under source/ for screenshot images, resizes
each screenshot down to the nearest accepted App Store canvas, then centers it
on that canvas. macOS screenshots keep transparent margins. iPhone, iPhone Duo,
and iPad screenshots use white margins, and watchOS screenshots use black
margins, because App Store Connect rejects transparency for those platforms.

A device screenshot exported onto a flat backdrop arrives with a border of that
one color around the device. It is cleared inward from the corners and cropped
away first, so the canvas margin meets the device itself rather than a box
around it. Pass --keep-surround to leave it.

The platform comes from the file or folder name: "watch", "iPhoneDuo" (or
"iPhone-Duo", "iPhone Duo"), "iPhone", "iPad", or "macOS".

Only the work that is actually needed runs: a screenshot whose generated PNG is
already newer than its source is left untouched, so a second run over an
unchanged source/ tree writes nothing. Pass --force to regenerate everything.
"""

from __future__ import annotations

import argparse
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

# The shared border code sits beside this script; python -I leaves this
# directory off the path, so it is put there explicitly.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from screenshot_surround import Surround, find_surround


# Canvases App Store Connect accepts, from Apple's screenshot specifications.
# iPhone is "iPhone with Dynamic Island (medium display)", the one iPhone size a
# submission must have; App Store Connect scales it for the others. iPhone Duo
# is the outer display (1398 x 2034) and the inner one (2007 x 2853); iPad is the
# required 13-inch display.
APP_STORE_SIZES = {
    "macos": [(1280, 800), (1440, 900), (2560, 1600), (2880, 1800)],
    "iphone": [(1179, 2556), (2556, 1179), (1206, 2622), (2622, 1206)],
    "iphoneduo": [(1398, 2034), (2034, 1398), (2007, 2853), (2853, 2007)],
    "ipad": [(2064, 2752), (2752, 2064), (2048, 2732), (2732, 2048)],
    "watchos": [(422, 514), (410, 502), (416, 496), (396, 484), (368, 448), (312, 390)],
}

# Platforms that App Store Connect requires to be opaque, and the margin color
# used to fill the canvas around each centered screenshot.
BACKGROUND_COLORS = {
    "iphone": "white",
    "iphoneduo": "white",
    "ipad": "white",
    "watchos": "black",
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
        "--force",
        action="store_true",
        help="Regenerate screenshots, even where the existing output is up to date.",
    )
    parser.add_argument(
        "--keep-surround",
        action="store_true",
        help="Keep a flat-colored border around the device instead of removing it.",
    )
    parser.add_argument(
        "--surround-fuzz",
        type=int,
        default=5,
        help=(
            "Tolerance percent when matching a flat border. Defaults to 5: a dark "
            "device rim can be only a few shades off a dark backdrop."
        ),
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
    # Separators dropped, so iPhoneDuo, iPhone-Duo, and "iPhone Duo" all match.
    # Checked before plain iPhone, whose name it contains.
    compact_name = re.sub(r"[^a-z0-9]", "", searchable_name)
    if "watch" in searchable_name:
        return "watchos"
    if "iphoneduo" in compact_name:
        return "iphoneduo"
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


def existing_outputs(output_dir: Path, source: Path) -> list[Path]:
    """Return screenshots already generated from this source, at any canvas size."""
    product_dir = output_dir / source.parent.name
    if not product_dir.is_dir():
        return []

    prefix = f"{source.stem}-appstore-"
    return sorted(
        path
        for path in product_dir.iterdir()
        if path.is_file() and path.suffix.lower() == ".png" and path.name.startswith(prefix)
    )


def output_size(output: Path) -> tuple[int, int] | None:
    """The canvas size an output's name records, as in Shot-appstore-1242x2688.png."""
    match = re.search(r"-appstore-(\d+)x(\d+)$", output.stem)
    if not match:
        return None
    return int(match[1]), int(match[2])


def is_up_to_date(source: Path, outputs: list[Path], platform: str) -> bool:
    """True when exactly one output exists for this source and it is no older.

    More than one match means an earlier run chose a different canvas size, so
    the superseded file still needs clearing out. An output at a size the
    platform no longer lists -- one made before the platform had sizes of its
    own -- is out of date whatever its age.
    """
    if len(outputs) != 1:
        return False
    if output_size(outputs[0]) not in APP_STORE_SIZES[platform]:
        return False
    return outputs[0].stat().st_mtime >= source.stat().st_mtime


def convert_screenshot(
    magick: str,
    source: Path,
    output: Path,
    platform: str,
    target: tuple[int, int],
    surround: Surround | None,
) -> None:
    target_width, target_height = target
    background = BACKGROUND_COLORS.get(platform, "none")
    output.parent.mkdir(parents=True, exist_ok=True)

    command = [
        magick,
        str(source),
        "-alpha",
        "set",
        *(surround.arguments if surround else []),
        "-resize",
        f"{target_width}x{target_height}>",
        "-background",
        background,
        "-gravity",
        "center",
        "-extent",
        f"{target_width}x{target_height}",
    ]

    if platform in BACKGROUND_COLORS:
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

    generated = 0
    skipped = 0

    for source in sources:
        outputs = existing_outputs(output_dir, source)
        platform = platform_from_path(source)

        if is_up_to_date(source, outputs, platform) and not args.force:
            skipped += 1
            print(f"skip: {outputs[0].name} is already up to date")
            continue

        width, height = image_size(magick, source)
        size_note = f"{width}x{height}"
        surround = None if args.keep_surround else find_surround(magick, source, args.surround_fuzz)
        if surround:
            width, height = surround.width, surround.height
            size_note += f", {width}x{height} inside its border"
        target = choose_target(platform, width, height)
        output = output_path(output_dir, source, target)
        background = BACKGROUND_COLORS.get(platform, "transparent")
        print(
            f"{source} -> {output} "
            f"({platform}, {size_note} -> {target[0]}x{target[1]}, {background})"
        )

        # An earlier run may have picked a different canvas for this screenshot.
        # Leaving both behind would upload two copies of the same shot.
        superseded = [path for path in outputs if path != output]
        for path in superseded:
            print(f"  removing superseded {path.name}")

        generated += 1
        if args.dry_run:
            continue

        convert_screenshot(magick, source, output, platform, target, surround)
        for path in superseded:
            path.unlink()

    if args.dry_run:
        print(f"Dry run complete: {generated} to generate, {skipped} already up to date.")
        return 0

    if not generated:
        print(f"Nothing to do: {skipped} screenshot(s) already up to date.")
        return 0

    print(f"Complete: {generated} generated, {skipped} skipped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
