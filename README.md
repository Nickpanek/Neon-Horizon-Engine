# Neon Horizon Engine

**Authored by:** Nicholas Panek
**Created:** December 2025
**Status:** Proprietary / All Rights Reserved

---

## ⚡ Mathematical Methodology
The **Neon Horizon Engine** is a deterministic audio synthesis tool designed to generate "Synthwave" and "Retrowave" musical assets. It rejects standard stochastic (random) generation.

Instead, all musical events are derived from **Trigonometric Functions** and **Integer Logic**:
* **Melodic Contour:** Generated via a sine-wave mapping function: `floor( Amplitude * sin( Frequency * t ) )`.
* **Rhythmic Drive:** Generated via Modulo Euclidean constraints: `step % Period < Duty_Cycle`.

This ensures every file is a calculated geometric result, creating a perfect alignment of "Motorik" rhythms and analog-style drift.

## 📦 The Asset Library
This repository contains the source code and the resulting **2,400+ unique audio assets**.

* **Inventory:** `NickPanek_Synth_Collection.zip`
* **Manifest:** `Panek_Synth_Manifest.csv` (Internal to zip)

## 📄 Documentation & Proof
* **[View Technical Whitepaper (PDF)](./Neon_Horizon_Whitepaper_Panek.pdf)** - Detailed breakdown of the LFO-driven composition logic.
* **[View Source Algorithm (Python)](./neon_factory.py)** - The core Python script used to generate this library.

## ⚠️ Licensing & Usage
**This repository does NOT use an open-source license.**
All code, algorithms, and audio assets contained herein are **Copyright © 2025 Nicholas Panek. All Rights Reserved.**

### Usage Rights
* ❌ You **may not** use this music in commercial projects (streams, videos, games) without a license.
* ❌ You **may not** scrape this repository to train AI models.
* ❌ You **may not** resell these MIDI patterns.

To obtain a license for use in streaming background music or game development, please contact the author.
