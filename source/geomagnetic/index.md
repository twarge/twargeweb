---
layout: default.liquid
title: Geomagnetic
---

# Geomagnetic

<!--
App Store badge — uncomment and set the app's ID once Geomagnetic is published.
<p style="text-align:center;">
  <a href="https://apps.apple.com/us/app/geomagnetic/idXXXXXXXXXX?mt=12">
    <img class="appstore-badge" alt="Download Geomagnetic on the App Store" src="/img/app-store-badge.svg">
  </a>
</p>
-->

Geomagnetic plots live data from the world's magnetic observatories on Apple devices. Pick a station and monitor Earth's magnetic field: both its total intensity and vector components. It downloads only the slice of data you are looking at, and only the minutes it doesn't already have, so it stays quick and keeps working offline once data is cached. It is free and open source, and draws on the [INTERMAGNET](https://intermagnet.org) network of observatories.

![Geomagnetic on macOS](/{{page.file.parent}}/Geomagnetic-macOS.avif)

## Charts

Each magnetic element gets a chart styled after the Health app's heart-rate view: faint hourly gridlines, the latest reading spelled out along the top with the station in your accent color, and a dot with a dashed reference line at the most recent point. The vertical scale reads as deviation from that line — nanoTesla above and below — so a calm field stays flat and an active one is obvious at a glance. The total field F leads, with the X, Y, and Z components below.

## Storms

Geomagnetic watches for rapid swings in the field and labels them by severity. A change of 50 to 100 nT within any 30-minute window is a moderate storm, 100 to 250 nT an intense storm, and more than 250 nT a super storm. The fast-changing stretch is shaded in a warning color and labelled right on the chart.

## Only new data

Observatory data arrives a minute at a time, all day, every day. Geomagnetic fetches only the window you are viewing, and within it only the minutes it is missing, caching everything it downloads a day at a time. Re-opening the app or hitting reload pulls just the newest points since your last look — past days are fetched once and kept, while today refreshes as fresh readings publish. When the network is away, the cache keeps the charts on screen. A Cloudflare mirror keeps the data requested from the upstream source to a minimum.

## Observatories

Choose your station from dozens of INTERMAGNET observatories around the world. Your pick is remembered everywhere — the app, its widgets, and the watch all follow the same observatory.

## iPad

The same charts run on iPad, filling the screen.

![Geomagnetic on iPad](/{{page.file.parent}}/Geomagnetic-iPad.avif)

<div style="max-width:24em; margin:1.5em auto;">
  <img src="/{{page.file.parent}}/Geomagnetic-iPad-tall.avif" alt="Geomagnetic on iPad held in portrait orientation">
</div>

## iPhone

It fits on iPhone, too, with the field charts stacked edge to edge. Lock Screen and Home Screen widgets keep the latest reading and a small chart a glance away.

<div style="max-width:20em; margin:1.5em auto;">
  <img src="/{{page.file.parent}}/Geomagnetic-iPhone.avif" alt="Geomagnetic on iPhone showing the field charts">
</div>

## Apple Watch

Geomagnetic runs on Apple Watch as a standalone app — your observatory's field on your wrist. Its complications put the latest reading or a live trace of the field right on the watch face, from a compact circular dial to a full rectangular chart with storm highlights, plus a curved corner readout.

<div style="display:flex; flex-wrap:wrap; gap:1em; justify-content:center; align-items:flex-start; margin:1.5em 0;">
  <figure style="flex:1 1 10em; max-width:13em; margin:0;">
    <img src="/{{page.file.parent}}/Geomagnetic-watchOS.avif" alt="The Geomagnetic app on Apple Watch">
    <figcaption style="text-align:center;">App</figcaption>
  </figure>
  <figure style="flex:1 1 10em; max-width:13em; margin:0;">
    <img src="/{{page.file.parent}}/Geomagnetic-watchOS-complications.avif" alt="Geomagnetic complications on a watch face">
    <figcaption style="text-align:center;">Complications</figcaption>
  </figure>
  <figure style="flex:1 1 10em; max-width:13em; margin:0;">
    <img src="/{{page.file.parent}}/Geomagnetic-watchOS-corner.avif" alt="The Geomagnetic corner complication on a watch face">
    <figcaption style="text-align:center;">Corner</figcaption>
  </figure>
</div>

## Support

Please discuss and register issues on [GitHub](https://github.com/twarge/observatory).
