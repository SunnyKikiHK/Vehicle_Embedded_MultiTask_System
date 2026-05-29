"""Skill loader: discovers skills at src/skills/ and parses their YAML frontmatter."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from src.constants import AGENT_MAPPING, SKILLS_ROOT, SERVER_USE


_SKILL_MANIFEST: dict[str, SkillManifest] | None = None

@dataclass
class SkillManifest:
    """
    Parsed metadata from a skill's SKILL.md YAML frontmatter.

    name: Skill slug, e.g. "hvac-agent".
    description: The full third-person description from the `description` field —
        this is the primary routing signal for the LLM.
    skill_dir: Absolute path to the skill's directory.
    """

    name: str
    description: str
    skill_dir: Path


def _parse_frontmatter(text: str) -> dict[str, str]:
    """
    Parse YAML frontmatter from a markdown file without requiring the `yaml` module.

    Extracts the ``name`` and ``description`` fields using regex, which is sufficient
    for our use case and avoids adding a dependency.

    Handles both standard ``---`` blocks and simple key: value YAML.

    Returns a dict with ``name`` and ``description`` keys (empty values if not found).
    """
    fm: dict[str, str] = {}

    # Match standard YAML frontmatter: --- ... ---
    match = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL | re.MULTILINE)
    if not match:
        return fm

    block = match.group(1)

    # Extract name field (value may be on the same line or next line)
    name_match = re.search(r"^name:\s*(.+?)\s*$", block, re.MULTILINE)
    if name_match:
        fm["name"] = name_match.group(1).strip()

    # Extract description field — handle multi-line values (quoted or after :)
    desc_match = re.search(r"^description:\s*(.+?)\s*$", block, re.MULTILINE)
    if desc_match:
        fm["description"] = desc_match.group(1).strip()

    return fm


def _build_manifest() -> dict[str, SkillManifest]:
    """Scan src/skills/, parse frontmatter, return dict slug → SkillManifest."""
    skills_root = Path(SKILLS_ROOT)
    manifests: dict[str, SkillManifest] = {}

    if not skills_root.exists():
        return manifests

    for skill_dir in skills_root.iterdir():
        if not skill_dir.is_dir():
            continue

        sk_path = skill_dir / "SKILL.md"
        if not sk_path.exists():
            continue

        try:
            text = sk_path.read_text(encoding="utf-8")
        except OSError:
            continue

        fm = _parse_frontmatter(text) #  with name and description
        name = fm.get("name", skill_dir.name)

        # Skip agents that are disabled in SERVER_USE
        if name not in SERVER_USE or not SERVER_USE[name]:
            continue

        description = fm.get("description", "")

        manifests[name] = SkillManifest(
            name=name,
            description=description,
            skill_dir=skill_dir
        )

    return manifests



_SKILL_MANIFEST: dict[str, SkillManifest] = _build_manifest()
# Formatting helpers (used by the router)
def format_skill_descriptions() -> str:
    """
    Build the agent routing section for the router prompt using skill
    frontmatter descriptions.

    Each skill's description is formatted as a markdown section with its
    description text, giving the LLM rich trigger-signal context for routing.

    Example output::

        ### HVAC Agent
        Implements HVAC (climate control) intents in the vehicle embedded
        multi-task system. Handles air conditioning, heating, defrosting,
        air quality, and ventilation systems. Use when the user mentions
        HVAC, air conditioning, temperature, fan, defog, defrost, AC,
        heating, cooling, ventilation, purifier, or recirculation.
        Trigger terms: 空调, 温度, 制冷, 制热, 风力, 除雾...

    """
    manifest = _SKILL_MANIFEST
    lines: list[str] = []

    # Sort deterministically by name for reproducible prompts
    for name in sorted(manifest):
        skill = manifest[name]
        # Derive a human-readable agent name from the skill slug:
        # "hvac-agent" → "HVAC Agent"
        # "user-profile-agent" → "User Profile Agent"
        # agent_name = _slug_to_agent_name(name)

        lines.append(f"### {name}")
        lines.append(skill.description.strip())
        lines.append("")

    return "\n".join(lines)


def _slug_to_agent_name(slug: str) -> str:
    """Convert a skill slug like 'hvac-agent' to 'HVAC Agent'."""
    if slug in AGENT_MAPPING:
        return AGENT_MAPPING[slug]

    # Generic fallback: "foo-agent" → "Foo Agent"
    base = slug.replace("-agent", "").replace("-", " ").strip()
    parts = base.split()
    return " ".join(p.capitalize() for p in parts) + " Agent"


def get_agent_names_from_skills() -> str:
    """Return a comma-separated list of agent names derived from skill slugs."""
    names = [_slug_to_agent_name(name) for name in _SKILL_MANIFEST]
    return ", ".join(sorted(names))



if __name__ == "__main__":
    enabled_agents = [k for k, v in SERVER_USE.items() if v]

    print("SkillLoader self-test\n")

    print("[Skill discovery]")
    print(f"  Found {len(_SKILL_MANIFEST)} enabled skills out of {len(SERVER_USE)} total:")
    for name in sorted(_SKILL_MANIFEST):
        skill = _SKILL_MANIFEST[name]
        print(f"  - {skill.name}, dir={skill.skill_dir.name}")

    print(f"\n[Enabled agents]: {', '.join(sorted(enabled_agents))}")
    print(f"[Disabled agents]: {', '.join(sorted([k for k, v in SERVER_USE.items() if not v]))}")

    print("\n[Agent names]")
    names = get_agent_names_from_skills()
    print(f"  {names}")

    print("\n[Formatting]")
    formatted = format_skill_descriptions()
    print(f"  Total characters: {len(formatted)}")
    print(f"  First 300 chars:\n{formatted[:300]}")

    # Verify HVAC Agent description is present and rich
    hvac = next((s for name, s in _SKILL_MANIFEST.items() if "hvac" in name), None)
    if hvac:
        print(f"\n[HVAC description (first 200 chars)]:\n{hvac.description[:200]}")
