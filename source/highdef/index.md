---
layout: default.liquid
title: HighDeF
---

# HighDeF

<p style="text-align:center;">
  <a href="https://apps.apple.com/us/app/highdef/id6781456671?mt=12">
    <img class="appstore-badge" alt="Download HighDeF on the App Store" src="/img/app-store-badge.svg">
  </a>
</p>

HighDeF views HDF5 files on Apple devices. Open an `.h5` file and browse its groups and datasets in the sidebar, then read any dataset as a table, a plot, or an image — whichever suits the data. HighDeF only reads the part of a dataset you are looking at, so even multi-gigabyte files open immediately and stay responsive. It is free and open source, and built on the [HDF5 library](https://www.hdfgroup.org/solutions/hdf5/).

![HighDeF on macOS](/{{page.file.parent}}/HighDeF-macOS-Plot.avif)

## Plots

Numeric datasets become plots. One- and two-column data is drawn as a line series; wider numeric data becomes a heatmap. Pan and zoom to explore — HighDeF resamples to the resolution of the view instead of drawing every point, so sweeping across millions of samples stays smooth. When a dataset carries a `time` or `sample_number` column, HighDeF uses it for the x axis automatically.

## Tables

Any dataset can be read as a table. Rows load in bounded windows as you scroll, so the table appears at once no matter how long the dataset is. For datasets with more than two dimensions, a control along the top steps through the extra dimensions one slice at a time.

## Images

Datasets shaped like pictures — a two-dimensional grid, or a grid of RGB or RGBA pixels — render as a proper image, scaled to fit the window.

## Live data

HighDeF watches the file on disk and reloads when it changes, picking up rows as they are written. That makes it handy for watching a data logger fill a file in real time, not just for inspecting finished ones — and it holds your place, keeping the selected dataset, view, and zoom where you left them.

## iPad

The same viewer runs on iPad and iPhone. Browse the hierarchy, scroll through tables, and pinch to zoom a plot.

![HighDeF on iPad](/{{page.file.parent}}/HighDeF-iPad.avif)

## Support

Please discuss and register issues on [GitHub](https://github.com/twarge/highdef).
