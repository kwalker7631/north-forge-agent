# What North Forge can actually do

Three years of TSC work went into this. The hard part of the docs is not listing buttons. It is saying, in plain language, that the assistant is supposed to **know when it does not know**.

This page is the public picture. Manufacturer procedures (Kyocera, and later Sharp / Ricoh / Xerox) live in a private edition.

## The job

North Forge is an on-demand expert for people who already work on machines, networks, and document systems. It is meant to sit next to a tech — not replace them.

It is built to cover the messy middle of a support call:

- Electro-mechanical devices (print / scan / finish / paper path / supplies)
- The PC and network the device is attached to (Windows, macOS, Linux)
- Accounting and pull-print stacks used in the field, including **PaperCut** and **MyKey**
- Other document-management and fleet tools the edition has been taught

When the edition has a procedure, it gives the next exact step.  
When it does not, it is supposed to **stop**, name the gap, and ask for the missing fact or a source — not invent a part number, a firmware level, or a “works on my machine” fix.

That gap behavior is the product. After the tech (or admin) supplies the missing research, it is written into memory / skills so the next session does not start from zero.

## What is in the box today

| Layer | What you get now |
|---|---|
| Engine | Hermes Agent: tools, memory, skills, cron, gateway, local or cloud models, Docker / SSH / other backends |
| Chassis | Portable checkout + sibling venv + `HERMES_HOME` on the same drive |
| Public overlays | Field-service voice, Pocket Penny, Pine Barron Farms |
| Private edition (admin) | TSC skills: intake, ticket, KB draft, escalation, fault log, training, vendor research |
| Honesty rules | Label fact vs guess. Do not fill holes with confident fiction. Ask for the missing evidence. Persist what you were just taught. |
| Hands | Terminal UI now. Messaging gateway (Telegram, Discord, Slack, and the rest) when you turn it on. |

Built-in *engine* tasks are numerous (files, terminal, browser, memory, cron, subagents). Built-in *TSC* tasks are the edition skill list, not a hidden second program.

## What it is not (yet)

Say these out loud so a demo does not overpromise:

- Not a magic hallucination “scanner.” It is a working rule: separate known / sourced / inferred / unknown, and refuse to ship a guess as a KB.
- Not a full graphical console. Deploy Console is admin-only for building sticks. Day-to-day is still the agent UI.
- Not a database product. Memory and files today; a real parts / ticket / KB database is planned.
- Graphing, slide decks, video, and image *generation as first-class TSC tools* are planned, not the current teammate path.
- Offline only works if a **local model** and the edition content are already on the stick. Cloud models need a network.

## Portable and Docker

- **USB / SSD:** plan on **8 GB or larger** for a full portable build (engine + venv + edition). A 256 KB stick cannot hold this. Use a normal thumb drive or an external SSD; size is not the limit once you are past that floor.
- **No install on the teammate PC** for the USB path. Double-click Start North Forge.
- **Docker / server:** the engine already runs in containers and remote backends. That is an admin / lab path, not what you hand a hotline tech on day one.
- **Windows is the supported teammate path today.** macOS / Linux can run the engine; the one-click stick story is Windows first.

## Roadmap (do not demo as shipped)

1. Database-backed KB / asset / ticket memory  
2. A real graphical workbench for techs who will not use a terminal  
3. First-class graph, presentation, video, and image tools in the TSC loop  
4. More manufacturer editions (Sharp, Ricoh, Xerox, custom fleets)  
5. Cleaner offline packs (local model + edition, no API)

## How to talk about it in one paragraph

North Forge is a portable technical-support assistant. The public repo is a working agent anyone can run. An administrator loads a private edition so the same stick can work a Kyocera (or later Sharp, Ricoh, Xerox) call across the device, the PC, and the print-management stack — and is trained to mark a hole instead of making one up. When you fill the hole, it keeps the answer.
