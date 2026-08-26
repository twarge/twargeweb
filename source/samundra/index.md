---
layout: default.liquid
title: Samundra
---

# Samundra

<p style="text-align:center;">
  <a href="https://apps.apple.com/us/app/samundra/id6800133831?mt=12">
    <img class="appstore-badge" alt="Download Samundra on the App Store" src="/img/app-store-badge.svg">
  </a>
</p>

Samundra reads Ocean Optics HR4000 spectrometers, including the HR4000CG, on macOS. Connect an instrument over USB and the window shows the live spectrum. Samundra speaks to the spectrometer directly using Apple's `IOUSBHost` framework, so no vendor drivers or third-party libraries are required. It is free and open source.

![Samundra on macOS](/{{page.file.parent}}/Samundra-macOS.avif)

## Features

- Live spectrum display with a visible-spectrum color gradient, hover readout of wavelength and counts, peak indicator, and saturation warning
- Pinch to zoom the wavelength axis, drag or two-finger pan to scroll, double-click to reset; settings and zoom state persist across launches
- Prominence-based peak detection with sub-pixel wavelength marks, controlled by sensitivity, anticipated width, and a peak count
- Optional reference lines from the NIST Atomic Spectra Database — 48,000 observed lines from 193 to 1105 nm, ions I through III — filtered by element, ionization state, and line strength
- Integration time from 3.8 ms to 10 s, scan averaging, and boxcar smoothing
- Electric-dark and detector-nonlinearity corrections using the calibration stored in the instrument's EEPROM
- Recording starts automatically whenever a spectrometer is connected
- Save (⌘S) writes a two-column CSV of wavelength and amplitude; ⌘C or right-click ▸ Copy Data puts the same CSV on the clipboard

## Requirements

An Ocean Optics HR4000 or HR4000CG connected by USB, and macOS 14 or later.

## Support

Samundra is free and open source under the Apache 2.0 licence. Please discuss and register issues on [GitHub](https://github.com/twarge/samundra/issues).

Atomic line identifications use data extracted from the [NIST Atomic Spectra Database](https://physics.nist.gov/asd): Kramida, A., Ralchenko, Yu., Reader, J., and NIST ASD Team, National Institute of Standards and Technology.

Samundra is an independent product and is not affiliated with, endorsed by, or sponsored by Ocean Optics.
