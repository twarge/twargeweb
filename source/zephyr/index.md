---
layout: default.liquid
title: Zephyr
---

# Zephyr

<p style="text-align:center;">
  <a href="https://apps.apple.com/us/app/zephyr-for-zulip/id6799832919?mt=12">
    <img class="appstore-badge" alt="Download Zephyr on the App Store" src="/img/app-store-badge.svg">
  </a>
</p>

Zephyr is a [Zulip](https://zulip.com) client for Mac, iPad, and iPhone. Zulip is a discussion system where conversations are organized by topics.

![Zephyr on macOS](/{{page.file.parent}}/Zephyr-macOS.avif)

## At home on every device

Zephyr employs OS features that web apps can't easily access to make interaction smooth. Mac and iPad support multiple windows — open a conversation in its own window, put a different server in each one. Also supports Quick Look for attachments and drag and drop in and out of the app. 

Most of Zulip is here: topics and channels, reactions, polls and to-do lists, message editing and moving, starred messages, reminders that resurface a message when you want it, drafts that sync across devices, muting and following, channel administration, and full-text search with Zulip's search operators. Plus the things a native app should add — a share extension, unread-count widgets, Shortcuts support, and previews rendered by your server so what you send is exactly what they see.

<div style="display:flex; flex-wrap:wrap; gap:1em; justify-content:center; margin:1.5em 0;">
  <img style="flex:1 1 16em; min-width:14em; max-width:26em; align-self:flex-start;"
       src="/{{page.file.parent}}/Zephyr-iPad-Combined.avif"
       alt="Zephyr on iPad showing the combined feed beside the channel sidebar">
  <img style="flex:1 1 16em; min-width:14em; max-width:26em; align-self:flex-start;"
       src="/{{page.file.parent}}/Zephyr-iPad-Channels.avif"
       alt="Zephyr on iPad showing the All Channels browser">
</div>

## Works offline

Zephyr keeps a local archive of your messages and reads it first. Open the app on a plane and your conversations are there; search runs against the local index; anything you send queues and goes out when the network returns (not when you realize you need to press a retry button). When the connection is flaky, views render instantly from the archive instead of waiting on a timeout.

## Search

One field does both jobs. Typing filters what you're looking at — channels and topics narrow with every keystroke, so most of the time you land on the conversation before finishing the word. As you type, Zulip's search operators are offered as tokens: a sender, a channel, messages with links or attachments.

<div style="display:flex; flex-wrap:wrap; gap:1em; justify-content:center; margin:1.5em 0;">
  <img style="flex:1 1 16em; min-width:14em; max-width:26em; align-self:flex-start;"
       src="/{{page.file.parent}}/Zephyr-iPad-Search1.avif"
       alt="Typing in Zephyr's search field filters channels and topics live, with Zulip's search operators offered as tokens">
  <img style="flex:1 1 16em; min-width:14em; max-width:26em; align-self:flex-start;"
       src="/{{page.file.parent}}/Zephyr-iPad-Search2.avif"
       alt="Zephyr's search results view after pressing Return, showing matching messages across history">
</div>

Hit Return and the same text becomes a real search: a results view over your message history, matches highlighted, each one a click from its full conversation. Recent searches stay in the sidebar for next time.

## Multiple servers

Add as many Zulip servers as you like — work, open source projects, communities. They stay connected concurrently: notifications arrive from all of them, unread counts aggregate across them, and on the Mac each window can show a different server side by side.

## Keyboard navigation

You can drive from the keyboard: jump anywhere with Open Quickly, walk messages and the sidebar with the arrow keys, reply, react, star, and search without touching the pointer. On iPad, hardware keyboards get the same treatment. If you find missing keyboard from the official app, open an issue on GitHub. 

## iPhone

The same channels, conversations, and search, on iPhone.

<div style="display:flex; flex-wrap:wrap; gap:1em; justify-content:center; margin:1.5em 0;">
  <img style="flex:1 1 11em; min-width:10em; max-width:16em; align-self:flex-start;"
       src="/{{page.file.parent}}/Zephyr-iPhone-Nav.avif"
       alt="Zephyr on iPhone showing the channel list">
  <img style="flex:1 1 11em; min-width:10em; max-width:16em; align-self:flex-start;"
       src="/{{page.file.parent}}/Zephyr-iPhone-Combined.avif"
       alt="Zephyr on iPhone showing the combined feed">
  <img style="flex:1 1 11em; min-width:10em; max-width:16em; align-self:flex-start;"
       src="/{{page.file.parent}}/Zephyr-iPhone-Channel.avif"
       alt="Zephyr on iPhone showing a channel conversation with the compose field">
</div>

## Support

Please discuss and register issues on [GitHub](https://github.com/twarge/zephyr/issues).
