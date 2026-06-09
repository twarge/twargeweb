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
