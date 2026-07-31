# Twarge Website!

Uses Cobalt! First, install rust via rustup; follow these instructions:

    https://rustup.rs

Then install cobalt using:

    cargo install cobalt-bin --force

To run a development server, be sure the ./build directory exists (and is empty), then:

    cobalt serve

And then navigate to http://localhost:1024 to view the site. 

Convert all images to AVIF using 

    magick mogrify -format avif -quality 85% *.heic

Replace PNGs in the source tree with AVIF versions using

    scripts/replace-source-pngs-with-avif.py

Generate App Store-ready screenshots using

    scripts/prepare-app-store-screenshots.py

Both scripts only do the work that is needed: images already converted are left
alone, and an output older than its source is regenerated. Add `--dry-run` to
see what would change, `--force` to redo everything anyway, or `--clean` to
empty the screenshot output directory first.

Device screenshots exported with white around the device edge get that white
made transparent during AVIF conversion, so they sit on the page background
rather than on a white block. Only white connected to the outside edge is
cleared, so a white document inside the device stays white. Use `--keep-white`
to leave the surround alone, or `--white-fuzz` to change how much of the
anti-aliased edge is taken (10% by default).

## License

Copyright 2026 Twarge LLC. Licensed under the Apache License, Version 2.0; see
[LICENSE](LICENSE) or https://www.apache.org/licenses/LICENSE-2.0.

Bundled third-party assets keep their own licenses: Fira Code
(`source/fonts/firacode/LICENSE-FiraCode.txt`) and Libertinus
(`source/fonts/libertinus/OFL.txt`) are both under the SIL Open Font License.
