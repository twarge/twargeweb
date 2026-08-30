---
layout: default.liquid
title: Sangam
---

# Sangam

Sangam is a Mac, iPad, and iPhone client for [Jitsi](https://jitsi.org) meetings. It speaks to a Jitsi server directly — XMPP signaling and WebRTC media, written in Swift — rather than loading the Jitsi Meet web app inside a web view. The video fills the window and the controls are a native toolbar along the bottom.

![Sangam on macOS](/{{page.file.parent}}/Sangam-macOS.avif)

Sangam is still in development. It runs meetings against a Jitsi deployment today, but reconnect behaviour and compatibility across server versions are unfinished, and there is no App Store release yet. The list below is what works now, not what is planned.

## In a meeting

- Speaker view or a grid of tiles; right-click a tile to pin it to the stage
- A sidebar listing participants, each with a live feed; double-click one on the Mac to open it in its own window
- Screen sharing — a display or a single window on the Mac, the whole device on iPhone and iPad
- Chat, reactions, raise hand, and polls
- Per-tile connection indicators taken from inbound RTP statistics
- Incoming video quality is a setting (180p, 360p, 720p, 1080p) rather than something inferred from the window size
- Background blur on the outgoing camera, using Apple's own segmentation
- Camera picker on the video button, and camera changes mid-meeting do not end the call
- Jitsi Meet's bare-key shortcuts — M, V, D, R, C, W — disabled while the chat field has focus
- The toolbar drops less-used buttons into a More menu as the window narrows

## Hosting and moderation

- Lobby support: knock and wait to be admitted, or watch the lobby and admit or deny as a moderator
- Set or clear a meeting password
- Remote mute, and audio/video moderation where participants ask before unmuting
- Breakout rooms: create them, move people between them, join and remove them
- Speaker stats — floor time per participant, during the meeting and after
- An invite link to copy or share

## Apple platform integration

- iOS: the meeting is a system call through CallKit, with a Live Activity showing the room, elapsed time, and mute state on the lock screen and in the Dynamic Island
- macOS: a menu bar item with microphone, camera, and hangup while a meeting is running
- Picture in Picture on both platforms
- Join a room, toggle mute, and leave from Siri, Spotlight, and Shortcuts
- `sangam:` meeting links and Handoff between devices
- Notifications for lobby knocks and chat messages when the app is in the background
- Noise suppression through WebRTC's audio processing; on macOS the app points you at the system's Voice Isolation microphone mode instead of claiming its own

## How it is built

- One Swift package implements the client side of the Jitsi protocol: XMPP over WebSocket, SASL and JWT authentication, MUC presence and source metadata, Jingle session negotiation, and the Colibri bridge channel
- Outgoing video is sent as three simulcast layers with matching RTX streams
- Native WebRTC and Metal rendering throughout — no WebKit, Chromium, or React Native anywhere in the meeting path
- The same code runs on all three platforms; AppKit and UIKit supply only the platform surfaces

## Requirements

macOS 14 or later on an Apple Silicon Mac, or iOS 17 or later. Sangam needs a Jitsi server to connect to; it is developed against a self-hosted deployment, and other servers or older releases may not work.
