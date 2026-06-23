---
layout: default.liquid
title: Typeset
---

# Typeset

<p style="text-align:center;">
  <a href="https://apps.apple.com/us/app/typeset-typst/id6781494180?mt=12">
    <img class="appstore-badge" alt="Download Typeset on the App Store" src="/img/app-store-badge.svg">
  </a>
</p>

Typeset compiles [Typst](https://typst.app) documents on Apple devices. You can use the spectacular [universe of packages](https://typst.app/universe/) to add content and style your documents. In addition to typst, Typeset integrates the [Tinymist](https://github.com/Myriad-Dreamin/tinymist) language server for autocomplete and command signature hints. Typeset is completely free and open source and always will be. Typeset is unaffiliated with Typst.

![Typeset on macOS](/{{page.file.parent}}/Typeset-macOS.avif)

A native Mac editor with your Typst source and a live PDF preview side by side. The preview keeps pace as you type, and clicking it jumps straight to the matching line of source.

## Language server

Typeset embeds the [Tinymist](https://github.com/Myriad-Dreamin/tinymist) language server, so the editor understands your document as you write it. Start typing and Typeset suggests the functions, parameters, and symbols that fit, including your own `#let` bindings and anything pulled in from a package.

![Autocomplete suggestions in Typeset](/{{page.file.parent}}/Typeset-macOS-Suggestion.avif)

Call a function and a signature hint shows its parameters and their types, so you don't have to keep the documentation open in another window.

![Function signature hints in Typeset](/{{page.file.parent}}/Typeset-macOS-Signature.avif)

## Sidebar

Flip the sidebar between your project's files, the document outline, and every label paired with a list of where it is referenced. The outline and reference list come straight from Tinymist, so they stay in step with your document. 

<div style="display:flex; flex-wrap:wrap; gap:1em; justify-content:center; align-items:flex-start; margin:1.5em 0;">
  <figure style="flex:1 1 9em; max-width:11em; margin:0;">
    <img src="/{{page.file.parent}}/Typeset-macOS-Sidebar-Files.avif" alt="Files tab in the Typeset sidebar">
    <figcaption style="text-align:center;">Files</figcaption>
  </figure>
  <figure style="flex:1 1 9em; max-width:11em; margin:0;">
    <img src="/{{page.file.parent}}/Typeset-macOS-Sidebar-Outline.avif" alt="Outline tab in the Typeset sidebar">
    <figcaption style="text-align:center;">Outline</figcaption>
  </figure>
  <figure style="flex:1 1 9em; max-width:11em; margin:0;">
    <img src="/{{page.file.parent}}/Typeset-macOS-Sidebar-References.avif" alt="References tab in the Typeset sidebar">
    <figcaption style="text-align:center;">References</figcaption>
  </figure>
</div>

Drag and drop files in, out, and reorgnaize. Drop images directly into the code.  

## Vertical

For vertical screens, Typeset can stack the views when the window gets narrow.

<div style="max-width:24em; margin:1.5em auto;">
  <img src="/{{page.file.parent}}/Typeset-macOS-Tall.avif" alt="Typeset in a tall macOS window with source stacked above the preview">
</div>

## Log

When a compile fails, the log says what went wrong and where, so you can get back to writing.

![The Typeset compile log on macOS](/{{page.file.parent}}/Typeset-macOS-Log.avif)

## No mystery meat

Typeset can edit and preview `.typ` files anywhere in your filesystem and should operate as the command-line Typst does. Typeset also identifies folders with a `.typeset` extension as a package that can be opened; this package format is required for iOS operation. The package contains nothing more than the files shown in the sidebar, a .typesetstate file and a .gitignore that ignores the former.

![Showing the contents of a Typeset package](/{{page.file.parent}}/Typeset-Document-Show-Contents.avif)

![The Typeset document format](/{{page.file.parent}}/Typeset-Document-Format.avif)

## iPad

The app also fully functional on iPad: 

![Typeset on iPad](/{{page.file.parent}}/Typeset-iPad-Wide.avif)

<div style="max-width:24em; margin:1.5em auto;">
  <img src="/{{page.file.parent}}/Typeset-iPad-Tall.avif" alt="Typeset on iPad held in portrait orientation">
</div>

## iPhone

It all fits on iPhone, too. Write your document, preview, and manage the files in your package.

<div style="display:flex; flex-wrap:wrap; gap:1em; justify-content:center; align-items:flex-start; margin:1.5em 0;">
  <figure style="flex:1 1 12em; max-width:15em; margin:0;">
    <img src="/{{page.file.parent}}/Typeset-iPhone-Code.avif" alt="Editing Typst source on iPhone">
    <figcaption style="text-align:center;">Code</figcaption>
  </figure>
  <figure style="flex:1 1 12em; max-width:15em; margin:0;">
    <img src="/{{page.file.parent}}/Typeset-iPhone-Preview.avif" alt="Full-screen document preview on iPhone">
    <figcaption style="text-align:center;">Preview</figcaption>
  </figure>
  <figure style="flex:1 1 12em; max-width:15em; margin:0;">
    <img src="/{{page.file.parent}}/Typeset-iPhone-Files.avif" alt="Managing package files on iPhone">
    <figcaption style="text-align:center;">Files</figcaption>
  </figure>
</div>

## Support

Please discuss and register issues on [GitHub](https://github.com/twarge/typeset). If you're feeling generous, consider supporting [Typst](https://typst.app/pricing/) directly by purchasing their web service or via [GitHub Sponsor](https://github.com/sponsors/typst).
