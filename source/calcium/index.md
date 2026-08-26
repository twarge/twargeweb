---
layout: default.liquid
title: Calcium
---

# Calcium

<p style="text-align:center;">
  <a href="https://apps.apple.com/us/app/calcium-text-calculator/id6795935652?mt=12">
    <img class="appstore-badge" alt="Download Calcium on the App Store" src="/img/app-store-badge.svg">
  </a>
</p>

<style>
  @font-face {
    font-family: "Fira Code";
    font-style: normal;
    font-weight: 400;
    font-display: swap;
    src: url("/fonts/firacode/FiraCode-Regular.woff2") format("woff2");
  }
  @font-face {
    font-family: "Fira Code";
    font-style: normal;
    font-weight: 700;
    font-display: swap;
    src: url("/fonts/firacode/FiraCode-Bold.woff2") format("woff2");
  }

  /* A Mac window, faked: the demo sits in it live. */
  .calcium-window {
    max-width: 720px;
    margin: 2em auto;
    border-radius: 12px;
    background: #ffffff;
    box-shadow: 0 22px 70px rgba(0, 0, 0, 0.22), 0 0 0 1px rgba(0, 0, 0, 0.08);
    overflow: hidden;
  }
  .calcium-titlebar {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 14px;
    background: linear-gradient(#f6f6f6, #efefef);
    border-bottom: 1px solid rgba(0, 0, 0, 0.07);
  }
  .calcium-titlebar .dot {
    width: 12px; height: 12px; border-radius: 50%;
    box-shadow: inset 0 0 0 0.5px rgba(0, 0, 0, 0.15);
  }
  .dot-close    { background: #ff5f57; }
  .dot-minimize { background: #febc2e; }
  .dot-zoom     { background: #28c840; }
  .calcium-titlebar .doc-title {
    flex: 1;
    text-align: center;
    /* Balance the traffic lights so the title truly centres. */
    margin-right: 52px;
    font: 13px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    color: #6e6e73;
  }
  /* No internal scrolling: the backdrop flows and gives the window its
     height, the textarea overlays it exactly, and the page's own scrollbar
     does the rest. The two stay the same height because they render the same
     text and the backdrop repaints on every keystroke. */
  .calcium-frame {
    position: relative;
  }
  .calcium-frame .backdrop,
  .calcium-frame textarea {
    box-sizing: border-box;
    margin: 0;
    border: none;
    padding: 22px 26px;
    font: 14px/1.5 "Fira Code", ui-monospace, SFMono-Regular, Menlo, monospace;
    font-variant-ligatures: contextual;
    white-space: pre-wrap;
    word-wrap: break-word;
    background: transparent;
  }
  /* The backdrop paints above the textarea, pointer-transparent, so its
     anchors are clickable; the caret draws beneath and shows through. */
  .calcium-frame .backdrop {
    color: #1d1d1f;
    pointer-events: none;
    min-height: 8em;
    position: relative;
    z-index: 1;
  }
  .calcium-frame .backdrop a { color: #0f6bd8; pointer-events: auto; }
  .calcium-frame .backdrop .dim { color: #86868b; opacity: 0.7; }
  .calcium-frame textarea {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    color: transparent;
    caret-color: #1d1d1f;
    outline: none;
    resize: none;
    z-index: 0;
  }
  .calcium-frame .prose   { color: #86868b; }
  .calcium-frame .raw     { color: #86868b; }
  .calcium-frame .heading { font-weight: 700; }
  .calcium-frame .comment { color: #61788f; }
  .calcium-frame .answer  { color: #86868b; }
  .calcium-frame .error   { color: #d0342c; }
  .calcium-frame .redef {
    text-decoration: underline wavy #e58900 1px;
    text-underline-offset: 3px;
  }
  .calcium-frame .tok-num { color: #0f6bd8; }
  .calcium-frame .tok-str { color: #8a5a00; }
  .calcium-frame .tok-kw  { color: #8a3fc9; }
  .calcium-frame .tok-fn  { color: #d63384; }
  .calcium-frame .tok-def { color: #0e8377; }
  .calcium-frame .tok-dir { color: #8a3fc9; }
  .calcium-frame .tok-op  { color: #86868b; }
  .calcium-frame .loading {
    position: absolute; inset: 0; display: grid; place-items: center;
    color: #86868b; font: 13px ui-monospace, monospace;
  }
</style>

<div class="calcium-window">
  <div class="calcium-titlebar">
    <span class="dot dot-close"></span>
    <span class="dot dot-minimize"></span>
    <span class="dot dot-zoom"></span>
    <span class="doc-title">Calcium Demo.calcium — Edit me!</span>
  </div>
  <div class="calcium-frame">
    <div class="backdrop" id="backdrop"></div>
    <textarea id="editor" spellcheck="false" autocapitalize="off"
              autocomplete="off" autocorrect="off"></textarea>
    <div class="loading" id="loading">loading the engine…</div>
  </div>
</div>

<script type="module" src="/{{page.file.parent}}/calcium.js"></script>
