"""Documentation contracts for the repository front door."""

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
README = REPO_ROOT / "README.md"
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)")


def test_readme_local_links_resolve() -> None:
    """Every relative link offered from the front door should exist."""
    targets = {
        target.split("#", 1)[0]
        for target in MARKDOWN_LINK.findall(README.read_text(encoding="utf-8"))
        if target and not target.startswith(("http://", "https://", "mailto:"))
    }

    assert targets
    missing = sorted(target for target in targets if not (REPO_ROOT / target).exists())
    assert not missing, f"README.md has broken local links: {missing}"
