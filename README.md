# North Forge

<p align="center">
  <img src="assets/banner.png" alt="North Forge" width="100%">
</p>

<p align="center">
  <strong>A portable technical-support assistant for the service desk.</strong><br>
  Plug in the drive, start it, and describe the problem in ordinary English.
</p>

<p align="center">
  <a href="START_HERE.md"><img src="https://img.shields.io/badge/Start-START_HERE.md-0B1F3A?style=for-the-badge" alt="Start here"></a>
  <a href="PRODUCT.md"><img src="https://img.shields.io/badge/Product-PRODUCT.md-1E3A5F?style=for-the-badge" alt="Product"></a>
  <a href="CAPABILITIES.md"><img src="https://img.shields.io/badge/Scope-CAPABILITIES.md-2563EB?style=for-the-badge" alt="Capabilities"></a>
  <a href="DOCS.md"><img src="https://img.shields.io/badge/Docs-DOCS.md-4B5563?style=for-the-badge" alt="Documentation"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License: MIT"></a>
</p>

---

North Forge is an **agentic conversational assistant for technical support
teams**, running on [Hermes Agent](https://github.com/NousResearch/hermes-agent)
(Nous Research's tool-calling LLM engine) with a Windows-first portable
launcher, a drive-local storage layout, and a Full/Basic tier gate on top. Under
the hood it is the same class of system as any Hermes deployment — file,
terminal, browser, memory, scheduling, and gateway tools driven by whatever
model you point it at, cloud or local — packaged so a non-technical teammate
can plug in a drive and start talking instead of configuring an agent runtime.

That packaging is deliberately split in two. **This repository is the
chassis** — the engine, the launcher, the tier/passcode gate, the declarative
cron-sync that keeps a skill's own schedule registered without anyone typing a
command, and a generic support voice with no manufacturer content in it.
Manufacturer procedures — fault-code trees, firmware history, the actual
field knowledge a tech needs — live in a separate **private edition**
(Kyocera today; other manufacturers can start from the [OEM template](editions/OEM.md))
that installs into this chassis as a Hermes profile. Neither half is much use
alone: the chassis without an edition is a competent generalist with nothing
manufacturer-specific to say, and an edition's knowledge only reaches a
teammate through this chassis's runtime, tiering, and launcher. The private
edition is closer to a key than a decoration — it is what turns a general
assistant into one that actually knows this manufacturer's equipment.

| Who | What they do |
|---|---|
| **Teammate** | Plug in a prepared drive, double-click **Start North Forge**, and talk normally. |
| **Administrator** | Builds and updates the drive, selects an AI service or local model, and installs the private edition. |
| **This repository** | Supplies the public runtime, launchers, Pocket Penny, Pine Barron Farms, and field-service voice. |
| **Private edition** | Supplies manufacturer procedures, skills, and templates. |

> **Important:** cloning this repository gives you the generic chassis, not the
> private Kyocera knowledge pack. North Forge can use a cloud AI service (an
> online service that answers the assistant) or a separately configured local
> model. Cloud services require internet access and may charge for use.

Maintained by **Kenneth C. Walker Jr.**

## Start here

### I was handed a prepared drive

1. Plug in the drive and open it in File Explorer.
2. Double-click **Start North Forge**.
3. Describe the device, the symptom, and what you already tried.
4. Type `/menu` if you get lost.

You do **not** need GitHub, Python, or a class. Do not format the drive.
Assigned drives normally use a label such as `GREGW-NORTH`.

**Preview**

```text
North Forge
> The copier can print, but scan to folder stopped this morning.

Let's check the connection and credentials in order. First, what model is it,
and does the destination PC still open the shared folder?
```

Tip: press **Ctrl+C** once to stop the terminal session. You can close the
window with **Alt+F4** after it stops.

### I am an administrator building from source

Use this path only for a lab machine or for preparing a drive. Finished teammate
drives should be built by the private deployment console, not by asking each
teammate to clone GitHub.

**You need:**

- Windows 10 or 11 with PowerShell 5.1 or newer
- An internet connection for the first installation
- Git for the clone command
- An 8 GB or larger USB drive or portable SSD
- Python 3.11 or newer when available; the bootstrap can fetch its own copy

Open **PowerShell**, then run:

```powershell
git clone https://github.com/kwalker7631/north-forge-agent.git
cd north-forge-agent
.\north-forge.cmd
```

The first launch creates the Python environment and data folder beside the
checkout, then starts the setup flow. Choose an AI provider (the service or
local program that supplies the model) when prompted. Later launches reuse that
setup. If `North-Forge-Setup.exe` is already present at the drive root, you can
double-click it instead.

To see which edition and version a prepared drive uses:

```powershell
scripts\nf-setup.ps1 -Show
```

Tip: in PowerShell, press **Up Arrow** to reuse the previous command. One-line
installers from the Hermes website install stock Hermes, not this North Forge
checkout.

## What is included

- The Hermes conversational agent runtime and command-line interface
- A Windows launcher that repairs its portable Python environment when needed
- Drive-local configuration, conversations, memories, and logs
- File, terminal, browser, memory, scheduling, gateway, TUI, and desktop
  capabilities inherited from Hermes
- Declarative cron sync (`scripts/nf_sync_cron.py`): any installed skill that
  declares a `cron:` block in its own `SKILL.md` gets that job registered
  automatically on every launch and right after provisioning — no manual
  `/cron add`, no model/provider pin, so it runs the same on Basic and Full tier
- Generic North Forge support voice and public example overlays

## What is not included

- Private manufacturer manuals, fault-code procedures, or customer data
- A guarantee that an AI answer is correct; technicians must verify safety- or
  business-critical steps
- A fully offline model; offline use requires an administrator to install and
  configure one separately
- A finished graphical teammate console; the current teammate path is terminal-first

See [CAPABILITIES.md](CAPABILITIES.md) for the shipped/not-yet inventory and
[PRODUCT.md](PRODUCT.md) for the short product boundary.

## Portable storage and privacy

The checkout, Python environment, and North Forge data folder live beside one
another on the portable drive. The launcher does not use Windows AppData for
this setup. It also rebuilds the environment when moving between incompatible
PCs; your data folder is kept separate.

Conversations, configuration, memories, logs, and saved credentials can remain
on the drive. Treat it like a work laptop: keep it physically secure, do not
commit its data folder to Git, and report a lost assigned drive. Content sent to
a cloud AI service is also subject to that service's privacy terms.

Do not rename the checkout folder casually: its name determines the neighboring
data-folder name. If a rename is detected, the launcher asks whether to reuse
the old data rather than choosing silently.

## Everyday commands

| Action | Command |
|---|---|
| Start | **Start North Forge** or `north-forge.cmd` |
| Show the in-session menu | `/menu` |
| Open this documentation set | `/readme` or `/readme north-forge-agent` |
| Open private Kyocera docs (when installed) | `/readme kyocera` |
| Start a clean conversation | `/new` |
| Select or repair the AI provider | `hermes model` |
| Run the full setup wizard | `hermes setup` |
| Check engine health | `hermes doctor` |
| Show the prepared-drive edition | `scripts\nf-setup.ps1 -Show` |

Command help text: **“Type `/menu` to see chat actions. Run `hermes --help` in
PowerShell to see administrator commands.”**

## Troubleshooting and logs

| What you see | What to do |
|---|---|
| Windows says `git` is not recognized | Install [Git for Windows](https://git-scm.com/download/win), reopen PowerShell, and retry. |
| Setup cannot download packages | Check the internet connection and company proxy, then run `.\north-forge.cmd` again. |
| The assistant opens but cannot answer | Run `hermes model` and confirm the selected provider and sign-in details. |
| Automatic repair fails | Open the neighboring `north-forge-agent-launcher.log`; it records the failed readiness check. |
| A conversation or setting appears missing after a folder rename | Restart with `north-forge.cmd` and choose **R** to reuse the detected data folder. Do not delete either folder. |

The portable data folder is normally named `north-forge-agent-data`. Runtime
logs are under `north-forge-agent-data\logs\`; the early launcher log is beside
the checkout. When asking for help, remove passwords, access keys, and customer
information before sharing a log.

## Repository map

| Path | Purpose |
|---|---|
| [`north-forge.cmd`](north-forge.cmd) | Windows entry point and portable-data setup |
| [`agent/`](agent/) | Conversation loop, prompts, memory, and provider handling |
| [`tools/`](tools/) | File, terminal, browser, and other agent capabilities |
| [`gateway/`](gateway/) | Telegram, Discord, Slack, and other messaging connections |
| [`apps/desktop/`](apps/desktop/) | Electron desktop application |
| [`ui-tui/`](ui-tui/) | Terminal user interface |
| [`skills/`](skills/) | Built-in instruction packs |
| [`editions/`](editions/) | Public edition structure and OEM template |
| [`website/`](website/) | Full Hermes engine documentation source |

Developers should read [CONTRIBUTING.md](CONTRIBUTING.md) and the nearest
`AGENTS.md` before editing an area. Use `scripts/run_tests.sh` rather than calling
`pytest` directly.

## Documentation

- [Documentation map](DOCS.md)
- [Why North Forge exists](START_HERE.md)
- [Current capabilities and limits](CAPABILITIES.md)
- [Learning and memory](LEARNING.md)
- [Hermes engine reference](https://hermes-agent.nousresearch.com/docs/)
- [Issues for this fork](https://github.com/kwalker7631/north-forge-agent/issues)

## Thanks

North Forge uses [Hermes Agent](https://github.com/NousResearch/hermes-agent)
by Nous Research and its contributors under the MIT license. Engine problems
that are not specific to this fork belong in the upstream Hermes project.
