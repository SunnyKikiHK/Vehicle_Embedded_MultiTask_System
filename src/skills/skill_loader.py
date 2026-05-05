"""Skill loader: discovers skills at src/skills/ and parses their YAML frontmatter."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from src.constants import AGENT_MAPPING

_SKILL_MANIFEST: dict[str, SkillManifest] | None = None

# Known exact mappings for all 14 agents
_KNOWN = AGENT_MAPPING


def get_skill_manifest() -> dict[str, SkillManifest]:
    """Lazy singleton: scan src/skills/ once and return all skill manifests."""
    global _SKILL_MANIFEST
    if _SKILL_MANIFEST is None:
        _SKILL_MANIFEST = _build_manifest()
    return _SKILL_MANIFEST


@dataclass
class SkillManifest:
    """
    Parsed metadata from a skill's SKILL.md YAML frontmatter.

    name: Skill slug, e.g. "hvac-agent".
    description: The full third-person description from the `description` field —
        this is the primary routing signal for the LLM.
    skill_dir: Absolute path to the skill's directory.
    intent_count: Approximate number of intents handled by this skill (parsed
        from SKILL.md body, falls back to 0 if not found).
    """

    name: str
    description: str
    skill_dir: Path
    intent_count: int = 0


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


def _count_intents(skill_dir: Path) -> int:
    """Rough count of intent rows in the skill's SKILL.md body (table rows)."""
    sk_path = skill_dir / "SKILL.md"
    if not sk_path.exists():
        return 0

    text = sk_path.read_text(encoding="utf-8")
    # Count markdown table rows that start with "| " (skip header/separator rows)
    count = sum(
        1
        for line in text.splitlines()
        if line.startswith("| ") and not re.match(r"^\|[-| :]+\|$", line)
    )
    # Subtract 1 for the description line (not a table row)
    return max(0, count - 1)


def _build_manifest() -> dict[str, SkillManifest]:
    """Scan src/skills/, parse frontmatter, return dict slug → SkillManifest."""
    skills_root = Path(__file__).parent
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

        fm = _parse_frontmatter(text)
        name = fm.get("name", skill_dir.name)
        description = fm.get("description", "")

        manifests[name] = SkillManifest(
            name=name,
            description=description,
            skill_dir=skill_dir,
            intent_count=_count_intents(skill_dir),
        )

    return manifests



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
    manifest = get_skill_manifest()
    lines: list[str] = []

    # Sort deterministically by name for reproducible prompts
    for name in sorted(manifest):
        skill = manifest[name]
        # Derive a human-readable agent name from the skill slug:
        # "hvac-agent" → "HVAC Agent"
        # "user-profile-agent" → "User Profile Agent"
        # "info-query-agent" → "Info Query Agent"
        agent_name = _slug_to_agent_name(name)
        lines.append(f"### {agent_name}")
        lines.append(skill.description.strip())
        lines.append("")

    return "\n".join(lines)


def _slug_to_agent_name(slug: str) -> str:
    """Convert a skill slug like 'hvac-agent' to 'HVAC Agent'."""
    if slug in _KNOWN:
        return _KNOWN[slug]

    # Generic fallback: "foo-agent" → "Foo Agent"
    base = slug.replace("-agent", "").replace("-", " ").strip()
    parts = base.split()
    return " ".join(p.capitalize() for p in parts) + " Agent"


def get_agent_names_from_skills() -> str:
    """Return a comma-separated list of agent names derived from skill slugs."""
    manifest = get_skill_manifest()
    names = [_slug_to_agent_name(name) for name in manifest]
    return ", ".join(sorted(names))



if __name__ == "__main__":
    print("SkillLoader self-test\n")

    manifest = get_skill_manifest()
    print("[Skill discovery]")
    print("  Found {} skills:".format(len(manifest)))
    for name in sorted(manifest):
        skill = manifest[name]
        print("  - {}: {} intents, dir={}".format(skill.name, skill.intent_count, skill.skill_dir.name))

    print("\n[Agent names]")
    names = get_agent_names_from_skills()
    print("  {}".format(names))

    print("\n[Formatting]")
    formatted = format_skill_descriptions()
    print(f"  Total characters: {len(formatted)}")
    print(f"  First 300 chars:\n{formatted[:300]}")

    # Verify HVAC Agent description is present and rich
    hvac = next((s for name, s in manifest.items() if "hvac" in name), None)
    if hvac:
        print(f"\n[HVAC description (first 200 chars)]:\n{hvac.description[:200]}")
