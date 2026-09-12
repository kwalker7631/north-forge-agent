# North Forge

<p align="center">
  <img src="assets/banner.png" alt="North Forge" width="100%">
</p>

<p align="center">
  <strong>A portable senior for the service desk.</strong><br>
  Built for people who still believe the work is worth doing well.
</p>

<p align="center">
  <a href="START_HERE.md"><img src="https://img.shields.io/badge/Start-START_HERE.md-0B1F3A?style=for-the-badge" alt="Start here"></a>
  <a href="CAPABILITIES.md"><img src="https://img.shields.io/badge/What%20it%20can%20do-CAPABILITIES.md-2563EB?style=for-the-badge" alt="Capabilities"></a>
  <a href="PRODUCT.md"><img src="https://img.shields.io/badge/Product-PRODUCT.md-1E3A5F?style=for-the-badge" alt="Product"></a>
  <a href="DOCS.md"><img src="https://img.shields.io/badge/Docs-DOCS.md-4B5563?style=for-the-badge" alt="Documentation"></a>
  <a href="ARCHITECTURE.md"><img src="https://img.shields.io/badge/Architecture-ARCHITECTURE.md-1E293B?style=for-the-badge" alt="Architecture"></a>
  <a href="LEARNING.md"><img src="https://img.shields.io/badge/Learning-LEARNING.md-4B5563?style=for-the-badge" alt="Learning"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License: MIT"></a>
</p>

---

This project exists because the job is hard and the tools we were handed were not honest enough.

A technician on a live call should not have to write an eight-thousand-character prompt. They should describe the device, the symptom, and what they already tried — the way they would tell a senior who has been on the floor. North Forge is that senior in a pocket: a drive you plug in, a window you start, a voice that stays with the work.

It is not a chatbot wearing a new jacket. It is years of technical-support instinct, compartmentalized so a teammate does not have to drink the whole firehose to clear one call. When the pack knows the next step, it gives it. When it does not, it says so. That is the point. Confidence without the page is not help.

The public repository is the **chassis**. The manufacturer pack — the real procedures, the templates, the shop memory — is a private edition an administrator loads onto the drive. Kyocera is first. Other makers can use the same slot.

Maintained by **Kenneth C. Walker Jr.**, for people who still take the desk seriously.

## What it can do

| It can | Meaning |
|---|---|
| Sit on the call with you | Device, paper path, finish, supplies, the PC, the network, PaperCut, MyQ, and the rest of the document stack the edition has been taught |
| Speak like the desk | Short. Ordered. Look first. Do not touch yet. Grab this. Name what is still unknown |
| Refuse to invent | Built to show a hole instead of filling it with a plausible paragraph |
| Keep what the shop teaches | When a senior supplies the missing page, that answer is supposed to stay |
| Live on a drive | USB or SSD. Eight gigabytes or larger. Memory travels with the stick |
| Work for the person holding it | Plug in. Start North Forge. Talk. `/menu` if you get lost |
| Carry an edition | Locked to one manufacturer for a teammate. Open for an administrator who must switch packs |
| Learn in the background | On an always-on admin PC, scheduled research can watch public product notes. A stick in a drawer does not pretend to study overnight |
| Travel to another maker | Sharp, Ricoh, Xerox, or an in-house fleet — same chassis, different private pack |

That is the power. Not a longer feature list. A tool that stays on the floor with you.

Full inventory and honest limits: **[CAPABILITIES.md](CAPABILITIES.md)**.

## Who this is for

| Who | What they do |
|---|---|
| **The technician** | Plug in a prepared drive, double-click **Start North Forge**, describe the job. No GitHub. No class. |
| **The administrator** | Builds the drive, chooses a cloud service or a local model, installs the private edition, hands it over. |
| **This repository** | Engine, Windows launcher, portable layout, public overlays (Pocket Penny, Pine Barron Farms, field-service voice). |
| **The private edition** | Manufacturer procedures, skills, templates, deploy console. That is the product. |

> **Important.** Cloning this repository gives you the chassis, not the private knowledge pack. A cloud model needs a network and may cost money. A local model has to be installed on purpose. Neither one is a license to skip verifying a safety-critical step.

## Start here

### I was handed a prepared drive

1. Plug in the drive and open it in File Explorer.
2. Double-click **Start North Forge**.
3. Describe the device, the symptom, and what you already tried.
4. Type `/menu` if you get lost.

Do not format the drive. Assigned labels look like `GREGW-NORTH`.

**Preview**

```text
North Forge
> The copier can print, but scan to folder stopped this morning.

Let's check the connection and credentials in order. First, what model is it,
and does the destination PC still open the shared folder?
```

Stop the session with **Ctrl+C**. Close the window with **Alt+F4** after it stops.

### I am building from source

Finished teammate drives should come from the private deploy console. This path is for a lab machine.

You need Windows 10 or 11, PowerShell 5.1 or newer, Git, internet for the first install, and an 8 GB or larger drive.

```powershell
git clone https://github.com/kwalker7631/north-forge-agent.git
cd north-forge-agent
.\north-forge.cmd
```

The first launch builds the environment beside the checkout. Choose a provider when asked. Later launches reuse that setup.

```powershell
scripts\nf-setup.ps1 -Show
```

One-liners on the Hermes website install stock Hermes, not this checkout.

## What is included — and what is not

**Included:** the conversational runtime, a Windows launcher that can repair its own environment, drive-local memory and logs, file and terminal and browser tools, scheduling, a messaging gateway, a terminal UI, and the public overlays.

**Not included here:** private manuals, fault-code shops, customer data, a promise that every answer is correct, a ready-made offline brain, or a finished graphical console for the tech.

See [CAPABILITIES.md](CAPABILITIES.md) and [PRODUCT.md](PRODUCT.md).

## Portable storage and privacy

The checkout, the Python environment, and the data folder live next to each other on the drive. Treat that drive like a work laptop. Do not commit the data folder. Report a lost assigned stick. Cloud providers have their own terms.

Do not rename the checkout folder casually. The neighboring data folder follows that name.

## Everyday commands

| Action | Command |
|---|---|
| Start | **Start North Forge** or `north-forge.cmd` |
| Menu | `/menu` |
| This documentation set | `/readme` or `/readme north-forge-agent` |
| Private edition docs (when installed) | `/readme kyocera` |
| New conversation | `/new` |
| Provider | `hermes model` |
| Setup wizard | `hermes setup` |
| Health | `hermes doctor` |
| What this drive is pinned to | `scripts\nf-setup.ps1 -Show` |

## Troubleshooting

| What you see | What to do |
|---|---|
| `git` is not recognized | Install [Git for Windows](https://git-scm.com/download/win), reopen PowerShell, retry |
| Setup cannot download | Check the network and proxy, run `.\north-forge.cmd` again |
| It opens but cannot answer | `hermes model` — confirm the provider |
| Repair fails | Read `north-forge-agent-launcher.log` beside the checkout |
| Settings vanished after a rename | Restart and choose **R** to reuse the old data folder |

Strip passwords and customer names before you share a log.

## Documentation

- [Documentation map](DOCS.md)
- [Why this exists](START_HERE.md)
- [Capabilities and limits](CAPABILITIES.md)
- [How it learns](LEARNING.md)
- [OEM template](editions/OEM.md)
- [Hermes engine reference](https://hermes-agent.nousresearch.com/docs/)

Developers: [CONTRIBUTING.md](CONTRIBUTING.md) and the nearest `AGENTS.md`. Run `scripts/run_tests.sh`.

## Thanks

The runtime is [Hermes Agent](https://github.com/NousResearch/hermes-agent) by Nous Research and contributors (MIT). That work is real. It is listed last so the first page is the job.

Engine issues that are not this fork belong upstream. Issues for North Forge: [this repository](https://github.com/kwalker7631/north-forge-agent/issues).
