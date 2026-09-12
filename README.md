# North Forge

<p align="center">
  <img src="assets/banner.png" alt="North Forge" width="100%">
</p>

<p align="center">
  <strong>Portable technical support assistant</strong><br>
  Your desk. Your pack. Ordinary English.
</p>

<p align="center">
  <a href="START_HERE.md"><img src="https://img.shields.io/badge/Start-START_HERE.md-0B1F3A?style=for-the-badge" alt="Start here"></a>
  <a href="PRODUCT.md"><img src="https://img.shields.io/badge/Product-PRODUCT.md-1E3A5F?style=for-the-badge" alt="Product"></a>
  <a href="CAPABILITIES.md"><img src="https://img.shields.io/badge/Scope-CAPABILITIES.md-2563EB?style=for-the-badge" alt="Capabilities"></a>
  <a href="LEARNING.md"><img src="https://img.shields.io/badge/Learning-LEARNING.md-4B5563?style=for-the-badge" alt="Learning"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License: MIT"></a>
</p>

---

North Forge is a **working assistant for technical support teams** — device, PC, network, and the document stack the edition has been taught. It is not a chatbot reskin.

The public repository is the chassis: launchers, portable runtime, and public overlays. The manufacturer pack (Kyocera today; other OEMs later) is a private edition an administrator loads onto the stick.

A teammate should never have to become a prompt engineer on a live call. They plug the stick in, double-click **Start North Forge**, and describe the job the way they would tell a coworker. When the pack does not have the page, it is supposed to say so — then keep the answer once someone supplies it.

| Layer | Role |
|---|---|
| **This repo** | Public chassis — engine, launchers, Pocket Penny, Pine Barron Farms, field-service voice |
| **Private edition** | The TSC pack. Procedures, skills, templates |
| **Teammate** | Plug in → Start North Forge → talk normally |
| **Admin** | Builds the stick. Teammates do not clone GitHub |

Maintained by **Kenneth C. Walker Jr.**

Documentation set: **[DOCS.md](DOCS.md)** · In session: `/readme north-forge-agent`

---

## Handed a stick?

1. Plug it in and open the drive.
2. Double-click **Start North Forge**.
3. Describe the device and the problem in ordinary English.
4. If you get lost, type `/menu`.

You do not need GitHub, Python, or a class. Do not format the stick.

Assigned sticks use a volume name of **FIRSTL-NORTH** (example: Greg Warhol → `GREGW-NORTH`). The agent name is optional. Default is North Forge.

---

## What runs on the drive

The checkout, the Python environment, and the data folder live **on the stick**, next to each other. Nothing is written into Windows AppData. Unplug it and take it to another PC.

Minimum media for a teammate stick: **8 GB**. Windows first. macOS and Linux can run the same checkout; the one-click story is Windows.

---

## Admin / lab — first start from this repo

Use this only if you are building from source. Finished sticks skip it.

```powershell
git clone https://github.com/kwalker7631/north-forge-agent.git
.\north-forge.cmd
```

Or double-click `North-Forge-Setup.exe` at the drive root when that file is present.

Requires Windows 10/11 and PowerShell 5.1+. Python 3.11+ if it is on PATH; otherwise bootstrap fetches its own.

Check what a stick is pinned to:

```powershell
scripts\nf-setup.ps1 -Show
```

Locked teammate sticks are built from the **private** deploy console, not by asking a tech to clone this repository.

One-liners on the Hermes website install **stock Hermes**, not this checkout. Use them only if you want plain Hermes on the PC.

---

## Everyday commands

| Action | Command |
|---|---|
| Start | **Start North Forge** or `north-forge.cmd` |
| Front door | `/menu` |
| This documentation set | `/readme` or `/readme north-forge-agent` |
| Kyocera edition docs | `/readme kyocera` |
| New conversation | `/new` |
| Engine health | `hermes doctor` |

Engine reference (gateway, tools, providers): [hermes-agent.nousresearch.com/docs](https://hermes-agent.nousresearch.com/docs/)

OEM template for another manufacturer: [editions/OEM.md](editions/OEM.md)

---

## Thanks

Runtime by [Hermes Agent](https://github.com/NousResearch/hermes-agent) / Nous Research and contributors (MIT). Listed last on purpose.

Issues for this fork: [kwalker7631/north-forge-agent](https://github.com/kwalker7631/north-forge-agent/issues)  
Engine issues: the upstream Hermes project.
