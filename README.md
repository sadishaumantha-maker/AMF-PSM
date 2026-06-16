# Anatomical Market Framework (AMF) v1.0

![License: Proprietary — All Rights Reserved](https://img.shields.io/badge/License-Proprietary-red)
![Status: Released](https://img.shields.io/badge/Status-v1.0%20Released-blue)

**Author:** Sadisha  
**Date of original creation:** March 17, 2026  
**Location:** Rathnapura, Sri Lanka

---

## What is the Anatomical Market Framework?

The Anatomical Market Framework (AMF) is an original analytical framework developed by Sadisha. It provides a structured approach to understanding and interpreting market dynamics through an anatomical lens — mapping the components, relationships, and behaviours of markets in a way that mirrors the systematic study of anatomy.

The framework maps a market's structure to biological analogues: infrastructure (skeleton), capital flow (circulatory system), information and signals (nervous system), active participants (musculature), functional subsystems (organs), risk management and regulation (immune system), and value creation and destruction (metabolism). The full methodology and applications are described in the documents below.

---

## Repository Contents

| File | Description |
|------|-------------|
| `AMF Framework v1.docx` | The full AMF framework document (Microsoft Word format) |
| `AMF Framework v1.docx.ots` | OpenTimestamps blockchain proof — cryptographically verifies the document existed on March 17, 2026 |
| `anatomical-market-framework` | Plain-text overview of the framework's seven core components and analytical method |
| `LICENSE.txt` | Proprietary copyright notice — all rights reserved |
| `CITATION.cff` | Machine-readable citation and authorship metadata |
| `CHANGELOG.md` | Release history of the framework |
| `SHA256SUMS` | SHA-256 checksums of the canonical artifacts, for integrity verification |
| `.github/workflows/integrity.yml` | CI workflow that verifies the artifact checksums on every change |

---

## Integrity, Provenance & Rights

This repository uses three independent, layered mechanisms to establish and protect authorship of the AMF:

### 1. Blockchain timestamp (OpenTimestamps)
The file `AMF Framework v1.docx.ots` is an **OpenTimestamps** proof. It cryptographically anchors the contents of `AMF Framework v1.docx` to the Bitcoin blockchain, providing independent, tamper-proof evidence that this exact version of the document existed on the date it was created.

To verify the timestamp independently:
1. Visit [https://opentimestamps.org](https://opentimestamps.org)
2. Upload both `AMF Framework v1.docx` and `AMF Framework v1.docx.ots` together
3. The site will confirm the timestamp against the Bitcoin blockchain

### 2. Checksums (SHA-256)
`SHA256SUMS` records the exact SHA-256 hash of each canonical artifact. Anyone can confirm a file has not been altered by running, from the repository root:

```sh
sha256sum --check SHA256SUMS
```

### 3. Continuous verification (CI)
The `Integrity` GitHub Actions workflow runs the checksum verification automatically on every push and pull request, so any unauthorized change to a protected file is detected immediately.

---

## License and Copyright

Copyright (c) 2026 Sadisha. **All Rights Reserved.**

This work is proprietary. No part of this framework or its associated documents may be reproduced, distributed, published, modified, adapted, translated, transmitted, or used in any form — commercial or non-commercial — without the **explicit prior written permission** of the author. Unauthorized use may result in civil and criminal liability under applicable copyright and intellectual property law.

See [`LICENSE.txt`](LICENSE.txt) for the full notice.

---

## Contact and Permissions

For permissions, licensing inquiries, or collaboration requests, please contact the author directly via GitHub ([@sadishaumantha-maker](https://github.com/sadishaumantha-maker)).
