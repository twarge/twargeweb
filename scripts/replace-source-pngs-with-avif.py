#!/usr/bin/env python3
"""Replace PNG images under source/ with AVIF versions, excluding favicons.

Only the work that is actually needed runs: a PNG whose AVIF is already at least
as new is left alone, and an AVIF older than its PNG is regenerated. Pass
--force to re-encode everything regardless.

Screenshots that arrive with a white surround around the device edge get that
white made transparent, so they sit on the page background instead of on a white
block. The white is flood filled inward from the four corners rather than
matched across the whole image, which keeps white that belongs to the screenshot
itself -- a document page inside the device stays white.

A device screenshot on a flat backdrop of another color -- a dark one, say -- has
that border cleared from the corners too, and is cropped to the device, so a
speck of capture debris at the edge goes with it. It is left alone unless the
backdrop shows on every side and clearing it leaves the device as one solid
region, which keeps a bare screenshot whose own background reaches its corners
intact. Pass --keep-surround to leave such a border.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

# The shared border code sits beside this script; python -I leaves this
# directory off the path, so it is put there explicitly.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from screenshot_surround import find_surround, probe_corners


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert PNGs under source/ to AVIF and remove each PNG after success, "
            "excluding favicon files."
        )
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("source"),
        help="Directory to scan recursively. Defaults to source/.",
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=85,
        help="AVIF quality passed to ImageMagick. Defaults to 85.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-encode every PNG, even where the .avif is already up to date.",
    )
    parser.add_argument(
        "--keep-png",
        action="store_true",
        help="Keep the original PNG after creating the AVIF.",
    )
    parser.add_argument(
        "--keep-white",
        action="store_true",
        help="Keep a white surround instead of making it transparent.",
    )
    parser.add_argument(
        "--white-fuzz",
        type=int,
        default=10,
        help=(
            "Tolerance percent when matching the white surround, which also "
            "catches the anti-aliased fringe along the device edge. Defaults to 10."
        ),
    )
    parser.add_argument(
        "--keep-surround",
        action="store_true",
        help="Keep a flat border of any other color around the device instead of removing it.",
    )
    parser.add_argument(
        "--surround-fuzz",
        type=int,
        default=5,
        help=(
            "Tolerance percent when matching a flat border of another color. "
            "Defaults to 5: a dark device rim can be only a few shades off a dark backdrop."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned replacements without writing or deleting files.",
    )
    return parser.parse_args()


def require_magick() -> str:
    magick = shutil.which("magick")
    if not magick:
        print("error: ImageMagick is required; install it so `magick` is on PATH.", file=sys.stderr)
        sys.exit(1)
    return magick


def is_favicon(path: Path) -> bool:
    return path.suffix.lower() == ".png" and path.stem.lower().startswith("favicon")


def png_sources(source_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in source_dir.rglob("*")
        if path.is_file() and path.suffix.lower() == ".png" and not is_favicon(path)
    )


def temporary_avif_path(target: Path) -> Path:
    return target.with_name(f".{target.stem}.tmp.avif")


def is_white_corner(pixel: tuple[float, ...], fuzz: int) -> bool:
    """True when this corner is opaque and close enough to white."""
    if len(pixel) < 3:
        return False

    # ImageMagick reports colour channels as 0-255 but alpha as 0-1.
    alpha = pixel[3] if len(pixel) > 3 else 1.0
    if alpha <= 0.5:
        return False

    return min(pixel[:3]) >= 255.0 * (1.0 - fuzz / 100.0)


def white_surround_arguments(width: int, height: int, fuzz: int) -> list[str]:
    """Flood fill white inward from each corner.

    Flooding from the corners, rather than matching white everywhere, only clears
    white that is connected to the outside edge. White inside the screenshot --
    a document page on screen, say -- is left alone.
    """
    arguments = ["-alpha", "set", "-fuzz", f"{fuzz}%", "-fill", "none"]
    corners = ((0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1))
    for x, y in corners:
        arguments.extend(["-floodfill", f"+{x}+{y}", "white"])
    return arguments


def is_up_to_date(source: Path, target: Path) -> bool:
    """True when the AVIF exists and is no older than the PNG it came from."""
    return target.exists() and target.stat().st_mtime >= source.stat().st_mtime


def convert_png(
    magick: str,
    source: Path,
    target: Path,
    quality: int,
    operators: list[str] | None = None,
) -> None:
    temporary_target = temporary_avif_path(target)
    if temporary_target.exists():
        temporary_target.unlink()

    try:
        subprocess.run(
            [
                magick,
                str(source),
                *(operators or []),
                "-quality",
                str(quality),
                str(temporary_target),
            ],
            check=True,
        )
        temporary_target.replace(target)
    except Exception:
        if temporary_target.exists():
            temporary_target.unlink()
        raise


def main() -> int:
    args = parse_args()
    magick = require_magick()

    if not args.source.exists():
        print(f"error: source directory does not exist: {args.source}", file=sys.stderr)
        return 1

    sources = png_sources(args.source)
    if not sources:
        print(f"No PNG files found under {args.source}; nothing to convert.")
        return 0

    converted = 0
    skipped = 0
    failed = 0

    for source in sources:
        target = source.with_suffix(".avif")

        if is_up_to_date(source, target) and not args.force:
            skipped += 1
            print(f"skip: {target.name} is already up to date")
            continue

        operators: list[str] = []
        surround_note = ""
        if not (args.keep_white and args.keep_surround):
            try:
                width, height, corners = probe_corners(magick, source)
                white = all(is_white_corner(corner, args.white_fuzz) for corner in corners)
                # A white surround is handled as it always was; only another
                # color goes through the stricter border check.
                surround = None
                if not white and not args.keep_surround:
                    surround = find_surround(magick, source, args.surround_fuzz)
            except (subprocess.CalledProcessError, ValueError) as error:
                print(f"warning: could not inspect {source}: {error}", file=sys.stderr)
            else:
                if white and not args.keep_white:
                    operators = white_surround_arguments(width, height, args.white_fuzz)
                    surround_note = ", white surround -> transparent"
                elif surround:
                    operators = surround.arguments
                    surround_note = (
                        f", border removed, cropped to the {surround.width}x{surround.height} device"
                    )

        action = "regenerating stale AVIF" if target.exists() else "creating AVIF"
        removal_note = "keeping PNG" if args.keep_png else "removing PNG"
        print(f"{source} -> {target} ({action}, {removal_note}{surround_note})")

        if args.dry_run:
            converted += 1
            continue

        try:
            convert_png(magick, source, target, args.quality, operators)
            converted += 1
            if not args.keep_png:
                source.unlink()
        except subprocess.CalledProcessError as error:
            failed += 1
            print(f"error: ImageMagick failed for {source}: {error}", file=sys.stderr)
        except OSError as error:
            failed += 1
            print(f"error: could not replace {source}: {error}", file=sys.stderr)

    if args.dry_run:
        print(f"Dry run complete: {converted} to convert, {skipped} already up to date.")
        return 0

    if not converted and not failed:
        print(f"Nothing to do: {skipped} PNG file(s) already converted.")
        return 0

    print(f"Complete: {converted} converted, {skipped} skipped, {failed} failed.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
