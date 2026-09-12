# North Forge

<p align="center">
  <img src="assets/banner.png" alt="North Forge" width="100%">
</p>

**A technical support assistant on a stick.** Not a chatbot with a new coat of paint.

You already have Google. Techs still type *what is an F248* and get a confident wrong paragraph. This checkout exists so they can talk like a coworker and get a short, honest next step — or a clear “I don’t have that page.”

Start here if you do not want a vendor tour: **[START_HERE.md](START_HERE.md)**  
What it is: **[PRODUCT.md](PRODUCT.md)** · What it can do: **[CAPABILITIES.md](CAPABILITIES.md)** · How it learns: **[LEARNING.md](LEARNING.md)**

```
Public repo     = working chassis (this repo)
Private edition = the real TSC pack (Kyocera today; other OEMs later)
Teammate job    = plug in → Start North Forge → talk normally
```

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License: MIT"></a>
</p>

---

## If someone handed you a stick

1. Plug it in.
2. Open the drive.
3. Double-click **Start North Forge**.
4. Type the model and the code the way you would tell the person next to you.
5. Lost? Type `/menu`.

Do not format the stick. You do not need GitHub, Python, or a class.

Volume names look like **GREGW-NORTH** (Greg Warhol). That is who the stick belongs to.

---

## What this repo is

A portable agent checkout you can run from a USB or SSD. The Python environment and data folder live **next to** the repo on that drive, not in Windows AppData, so you can unplug it and take it to another PC.

Manufacturer procedures (Kyocera field steps, PaperCut, MyQ, and the rest) live in a **private edition**. This public tree is the engine, the launchers, and a few public overlays (Pocket Penny, Pine Barron Farms, field-service voice).

It is built on [Hermes Agent](https://github.com/NousResearch/hermes-agent) by Nous Research (MIT). That work is real. It is thanked at the bottom on purpose. The person holding the stick should not have to care what the engine is called.

Maintained by Kenneth C. Walker Jr.

---

## Windows — first start from this repo

**If you were handed a finished stick, skip this.** Use Start North Forge.

Admin / lab path:

1. Clone this repo onto the drive (or copy the folder).
2. Double-click `north-forge.cmd` in the repo root. First run builds the venv (~1 minute). Later runs just start.
3. Or use `North-Forge-Setup.exe` at the drive root if that file is present.

```powershell
git clone https://github.com/kwalker7631/north-forge-agent.git
.\north-forge.cmd
```

Needs Windows 10/11 and PowerShell 5.1+. Python 3.11+ if it is on PATH; otherwise the bootstrap fetches its own.

A locked teammate stick is built with the **private** deploy console, not by asking a tech to clone GitHub.

---

## Drive class and setup

What the stick is pinned to (Kyocera, Penny, and so on) lives on the drive. Check it with:

```powershell
scripts\nf-setup.ps1 -Show
```

Some editions let you change the agent nickname and model from that setup. Others are locked on purpose. If the menu is not there, it is already wired — just start it.

---

## Commands you will actually use

| Do this | Type |
|---|---|
| Start talking | double-click Start North Forge, or `north-forge.cmd` |
| Front door | `/menu` |
| New conversation | `/new` |
| Engine help | `hermes doctor` |

Engine docs (installers, gateway, tools): [hermes-agent.nousresearch.com/docs](https://hermes-agent.nousresearch.com/docs/)

The one-liners on the Hermes site install **stock Hermes**, not this fork. Use them only if you want plain Hermes on the PC. To run **this** checkout, use the drive-native path above.

---

## Other OEMs

The same chassis can carry a Sharp, Ricoh, or Xerox pack later. See [editions/OEM.md](editions/OEM.md).

---

## Thanks

Runtime by [Hermes Agent](https://github.com/NousResearch/hermes-agent) / Nous Research and contributors (MIT). Listed last on purpose.

Issues for this fork: https://github.com/kwalker7631/north-forge-agent/issues  
Engine issues: the upstream Hermes project.
