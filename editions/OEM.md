# OEM / manufacturer editions

North Forge's power is not a new agent loop. It is **an edition**: identity + skills + templates that an admin pins onto the public engine.

Kyocera is the first vertical. The same slot can hold Sharp, Ricoh, Xerox, Konica Minolta, HP, or an in-house fleet brand. The public repo never carries that proprietary content.

## Public vs private

| Lives in | Examples | Visible on GitHub |
|---|---|---|
| `editions/` in this repo | field-service voice, Pocket Penny, Pine Barron Farms | Yes |
| `private-editions/<name>/` (gitignored) | Kyocera TSC, future Sharp TSC, paid customizations | No — separate private repo |

`scripts/nf-setup.ps1` looks in `editions/<name>/` first, then `private-editions/<name>/`. Same pin command either way.

## How to cut a new manufacturer edition

1. Copy `editions/_oem-template/` to a **new private repo**. Do not commit manufacturer IP into this public repo.
2. Rename the folder and the `name:` field in `distribution.yaml` (`sharp`, `ricoh`, `xerox`, …).
3. Rewrite `SOUL.md` for that support organization (voice, what not to invent, what to collect).
4. Add skills. Start from the Kyocera catalog (private repo) and swap product names, portals, and templates:
   - intake / assist
   - hotline-ticket
   - kb-builder + that brand's locked HTML/template
   - escalation-packet
   - fault-logging
   - training-guide
   - sales-assist (if you sell as well as support)
5. Clone onto an admin PC:

   ```
   git clone <private-url> private-editions/sharp
   ```

6. Pin a stick (or use the Deploy Console and choose that pin):

   ```
   scripts\nf-setup.ps1 -NonInteractive -Tier basic -Pin sharp -Installed sharp -SetPasscode
   ```

Locked (`basic`) sticks cannot leave that manufacturer. Open (`full`) sticks can switch if you installed more than one.

## What you are selling later

- The **engine** stays free (MIT, this repo).
- The **edition** is the product: skills, templates, validated procedures, admin deploy, updates.
- Custom work (a Xerox fleet pack, a dealer-group overlay) is another private edition, not a fork of the engine.

Do not fork `north-forge-agent` per customer. Fork or clone the **edition** repo.
