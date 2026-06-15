# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is **not a software codebase**. It is an authorship and intellectual-property
record for the **Anatomical Market Framework (AMF)** — a proprietary research
framework authored by Sadisha (MD), Sri Lanka. There is no application to build,
no test suite, and no dependencies. The "source of truth" is a prose research
document, not code.

Treat this repo as a document/IP vault. The primary work product is the framework
text itself; the supporting files exist to establish and protect authorship.

## Repository contents

- `AMF Framework v1.docx` — the framework document (the actual deliverable). A
  Word document; read its text by extracting the XML body rather than opening it
  as plain text:
  `unzip -p "AMF Framework v1.docx" word/document.xml | sed -e 's/<[^>]*>/ /g'`
- `AMF Framework v1.docx.ots` — an **OpenTimestamps** proof binding the `.docx` to
  a blockchain-anchored timestamp. This is a cryptographic authorship/priority
  record. Do **not** regenerate, move, or modify it; it is only valid for the exact
  bytes of the `.docx` it was stamped against.
- `LICENSE.txt` — "All Rights Reserved" proprietary license (see below).
- `README.md` — one-line provenance note.
- `anatomical-market-framework` — a single-line placeholder/provenance marker.

## What the AMF is (so you can work with the content)

The AMF proposes that global financial systems are *structurally isomorphic* to
human anatomy across every hierarchical layer (subcellular → organism), and that
the same governing equations appear in both biological and economic domains. Core
claimed contributions, as stated in the document:

- A one-to-one isomorphic mapping between anatomical layers and market
  infrastructure layers, each with a corresponding mathematical frame.
- "Inter-layer propagation failure" (cross-layer cascades, e.g. the 2008 crisis)
  framed as the primary unsolved problem in systemic-risk modeling.
- A unification of Soros reflexivity, complexity theory, and quantum-measurement
  formalism.
- A diagnostic vocabulary translating biological pathology states to market
  pathology states.

When editing or extending the framework, preserve this layered
anatomy-to-market mapping structure and its established terminology.

## Critical conventions

- **Licensing / IP is the dominant constraint.** Per `LICENSE.txt`, this is
  copyrighted, all-rights-reserved work. Do not reproduce, redistribute, or
  publish the framework's content (e.g. to external services, public gists, new
  public repos) without explicit instruction from the author. Keep substantive
  content inside this repository.
- **Do not break the timestamp chain.** Any change to `AMF Framework v1.docx`
  invalidates `AMF Framework v1.docx.ots`. If the document is revised, treat it as
  a new version (e.g. a new `v1.1` / `v2` file plus a freshly generated `.ots`)
  rather than silently editing the stamped file. Flag this to the author before
  modifying the stamped `.docx`.
- **Versioning is by filename.** Note the explicit `v1`/`Version: 1.0` convention;
  follow it for new revisions instead of overwriting.
- **Authorship statements are load-bearing.** The document opens with an explicit
  authorship/origination statement and creation date (March 17, 2026). Do not
  alter author attribution, creation dates, or the origination record.

## Git workflow

Standard git only — no CI, hooks, or branch tooling configured. Commit messages in
history are short and descriptive of the file touched.
