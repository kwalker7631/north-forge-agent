# OEM edition template

This folder is a blank manufacturer pack.

1. Copy the whole folder into a **private** git repository.
2. Change `distribution.yaml` `name:` to the slug (`sharp`, `ricoh`, `xerox`, …).
3. Edit `SOUL.md`.
4. Add one folder per skill under `skills/`, each with a `SKILL.md`.
5. Clone that private repo into `north-forge-agent/private-editions/<slug>/`.
6. Pin with `nf-setup.ps1` or the Deploy Console.

See `editions/OEM.md` in the public engine for the full path.
The Kyocera private repo is the worked example — copy its skill list, not its Kyocera text, unless you have the rights.
