#!/usr/bin/env python3
"""Replace PNG images under source/ with AVIF versions, excluding favicons."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


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
        help="Overwrite existing .avif files with regenerated versions.",
    )
    parser.add_argument(
        "--keep-png",
        action="store_true",
        help="Keep the original PNG after creating the AVIF.",
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


def convert_png(magick: str, source: Path, target: Path, quality: int, force: bool) -> None:
    if target.exists() and not force:
        raise FileExistsError(f"{target} already exists; rerun with --force to overwrite it")

    temporary_target = temporary_avif_path(target)
    if temporary_target.exists():
        temporary_target.unlink()

    try:
        subprocess.run(
            [magick, str(source), "-quality", str(quality), str(temporary_target)],
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
        print(f"No PNG files found under {args.source}")
        return 0

    converted = 0
    skipped = 0
    failed = 0

    for source in sources:
        target = source.with_suffix(".avif")
        removal_note = "keeping PNG" if args.keep_png else "removing PNG"
        print(f"{source} -> {target} ({removal_note})")

        if args.dry_run:
            continue

        try:
            convert_png(magick, source, target, args.quality, args.force)
            converted += 1
            if not args.keep_png:
                source.unlink()
        except FileExistsError as error:
            skipped += 1
            print(f"skip: {error}", file=sys.stderr)
        except subprocess.CalledProcessError as error:
            failed += 1
            print(f"error: ImageMagick failed for {source}: {error}", file=sys.stderr)
        except OSError as error:
            failed += 1
            print(f"error: could not replace {source}: {error}", file=sys.stderr)

    if args.dry_run:
        print(f"Dry run complete: {len(sources)} PNG file(s) found.")
        return 0

    print(f"Complete: {converted} converted, {skipped} skipped, {failed} failed.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
