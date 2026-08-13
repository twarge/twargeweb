---
layout: default.liquid
title: Profiler
---

# Profiler

Profiler is a laser beam profiler for macOS and iPadOS that uses any PTP webcam as the sensor. Connect a camera and the window shows the live beam with horizontal and vertical profiles, ISO 11146 second-moment widths, centroid, ellipticity and azimuth. It is free and open source.

![Profiler on macOS](/{{page.file.parent}}/Profiler-macOS.avif)

Inputs are on the left, measurements on the right. The horizontal profile sits above the image and the vertical profile beside it, sharing the image's extent and one amplitude scale.

Tested with a Sony α7C, but should work with any camera that provides a video source, PTP or UVC.

## Features

- ISO 11146 D4σ widths — horizontal, vertical, principal-axis major and minor — with centroid, ellipticity, and azimuth in lab convention
- Three sources: Sony PC Remote over PTP with full ISO and shutter control, USB Streaming (UVC) at 1080p, and a synthetic beam with known ground truth shown alongside the measurement
- Auto-gain servo holds the peak at a target fraction of full scale, correcting immediately on saturation and walking up gently when under-exposed
- Saturation, clipped-pixel fraction, and background mean and σ reported every frame, with a warning over the image when clipping invalidates the measurement
- Dark-frame subtraction over 16 averaged frames; noise threshold and aperture factor sized per ISO 11146-1 and converged on the centroid
- Levenberg–Marquardt Gaussian fit on each marginal profile with interpolated FWHM
- Time-series plots of any metric, over a history window of 10 seconds to 10 minutes
- Nine colormaps including Turbo and Viridis, logarithmic scale, display gain, 1/e² ellipse with major-axis tick, and centroid crosshair
- µm/pixel calibration, with a one-click bare-sensor pitch for a lens-free α7C
- Per-channel analysis — green has twice the sampling density of red or blue on a Bayer sensor, so pick the channel matching your wavelength
- Share exports the beam image as PNG, both profiles as CSV, and the metrics as JSON; the image and either profile chart also drag straight out of the window
- Settings are stored per camera, keyed to the device, because µm/pixel describes the optical setup rather than a global preference

![Profiler on iPadOS](/{{page.file.parent}}/Profiler-iOS.avif)

## Requirements

macOS 14 or later, or iPadOS 17 or later. A Sony α7C connected by USB in PC Remote or USB Streaming mode, or any UVC camera. No vendor SDK or driver is needed — the app speaks PTP through Apple's `ImageCaptureCore` pass-through API.

On macOS, set Image Capture's *Connecting this camera opens:* to **No application** and quit Photos first. PTP allows one session per device, so anything else holding the camera blocks Profiler.

## Support

Profiler is free and open source under the Apache 2.0 licence. Please discuss and register issues on [GitHub](https://github.com/twarge/profiler).
