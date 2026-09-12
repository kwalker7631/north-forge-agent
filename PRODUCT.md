# North Forge is a technical support assistant

This is not Hermes Agent with a new name and a banner.

**Hermes Agent** (Nous Research, MIT) is the *engine*: memory, tools, models, terminal, gateway.  
**North Forge** is the *product*: a portable on-demand expert for technical support. An administrator loads real procedures — devices, PCs, PaperCut, MyKey, the rest of the document stack — and hands a tech a stick that is trained to **name a knowledge gap instead of inventing an answer**.

Anyone can clone this public repo and get a working agent.  
An administrator can add a **private edition** (Kyocera today; Sharp, Ricoh, Xerox, or any other vertical tomorrow) and ship a stick that actually knows that company's support work.

Read [CAPABILITIES.md](CAPABILITIES.md) for domain, honesty rules, portable/Docker limits, and the roadmap.

```
Public engine          = this repository (free to run)
Public overlays        = editions/penny-pincher, pine-barron-farms, field-service
Private vertical       = a separate repo cloned into private-editions/<name>
Admin deploy console   = lives with the private vertical (Kyocera: Advanced/deploy-console)
Teammate experience    = plug in USB → double-click Start North Forge → type English
```

## What a tech actually gets

Not a chatbot demo. A working assistant that can:

- Work a call across the device, the workstation (Windows / macOS / Linux), and print-management tools the edition knows
- Take a hotline / ticket in a fixed order
- Draft a knowledge-base article to a locked template
- Build an escalation packet with the evidence that is present
- Stop and ask when the procedure or the part number is not in the edition
- Keep the answer after you supply the missing research
- Stay inside technician judgment — it does not replace the tech

Those skills are not in the public chassis. They live in the **edition**. The Kyocera edition is the reference implementation. Copy that shape for another manufacturer.

## Two doors

| Door | Who | What they get |
|---|---|---|
| Public GitHub | Anyone | Working North Forge agent, portable on a USB, generic chassis voice |
| Admin edition | Licensed / private | Manufacturer skills, KB templates, deploy console, locked teammate sticks |

Monetization, when it comes, sits on the **second door**: specialized skills and admin deployment, not on the engine. The engine stays MIT. Vertical content stays yours (or your customer's).

## Not a reskin — the test

If you strip the banner, the CLI name, and `SOUL.md`, and the product still does Kyocera (or Sharp, or Ricoh) intake, KB, and escalation the same way a senior TSC would — it is North Forge.  
If all that remains is a general agent, you are looking at the engine only.

Read [editions/OEM.md](editions/OEM.md) to cut a new manufacturer edition.  
The Kyocera skill list and admin path live in the private edition repo, not here.
