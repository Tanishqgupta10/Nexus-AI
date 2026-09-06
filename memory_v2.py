"""
NEXUS AI — Persistent Memory 2.0
Lightweight local memory for facts, preferences, conversation summaries,
and relevant-memory retrieval. No external API required.
"""

import json
import re
from pathlib import Path
from datetime import datetime

MEMORY_FILE = "memory.json"
FACTS_FILE = "facts.json"
SUMMARY_FILE = "memory_summary.json"

MAX_MESSAGES = 80
MAX_NOTES = 100
MAX_SUMMARY_ITEMS = 30


def _load_json(path, default):
    try:
        p = Path(path)
        if not p.exists():
            return default
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return default


def _save_json(path, data):
    try:
        Path(path).write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return True
    except Exception:
        return False


def load_messages():
    data = _load_json(MEMORY_FILE, [])
    return data if isinstance(data, list) else []


def save_messages(messages):
    clean = []
    for message in messages[-MAX_MESSAGES:]:
        if not isinstance(message, dict):
            continue
        role = message.get("role")
        content = str(message.get("content", "")).strip()
        if role in ("user", "assistant") and content:
            clean.append({"role": role, "content": content})
    return _save_json(MEMORY_FILE, clean)


def load_facts():
    data = _load_json(FACTS_FILE, {})
    if not isinstance(data, dict):
        data = {}
    data.setdefault("notes", [])
    data.setdefault("preferences", [])
    return data


def save_facts(facts):
    return _save_json(FACTS_FILE, facts)


def update_facts(text):
    """Store only explicit user facts/preferences."""
    facts = load_facts()

    name_match = re.search(r"\bmy name is\s+(.+)", text, re.I)
    if name_match:
        facts["name"] = name_match.group(1).strip().rstrip(".!?")

    remember_match = re.search(r"\bremember that\s+(.+)", text, re.I)
    if remember_match:
        note = remember_match.group(1).strip().rstrip(".!?")
        if note:
            notes = facts.setdefault("notes", [])
            if note not in notes:
                notes.append(note)
                facts["notes"] = notes[-MAX_NOTES:]

    preference_patterns = [
        r"\bi prefer\s+(.+)",
        r"\bi like\s+(.+)",
        r"\bi don't like\s+(.+)",
        r"\bmy preference is\s+(.+)",
    ]
    for pattern in preference_patterns:
        match = re.search(pattern, text, re.I)
        if match:
            pref = match.group(0).strip().rstrip(".!?")
            prefs = facts.setdefault("preferences", [])
            if pref not in prefs:
                prefs.append(pref)
                facts["preferences"] = prefs[-MAX_NOTES:]
            break

    facts["updated_at"] = datetime.now().isoformat(timespec="seconds")
    save_facts(facts)
    return facts


def get_memory_context(query="", max_items=8):
    """Return relevant explicit memory plus a few recent user topics."""
    facts = load_facts()
    messages = load_messages()

    candidates = []

    if facts.get("name"):
        candidates.append(f"User name: {facts['name']}")

    for note in facts.get("notes", []):
        candidates.append(f"User fact: {note}")

    for pref in facts.get("preferences", []):
        candidates.append(f"User preference: {pref}")

    query_words = set(re.findall(r"[a-zA-Z0-9']+", query.lower()))

    scored = []
    for item in candidates:
        item_words = set(re.findall(r"[a-zA-Z0-9']+", item.lower()))
        scored.append((len(query_words & item_words), item))

    scored.sort(key=lambda x: x[0], reverse=True)
    selected = [item for score, item in scored if score > 0][:max_items]

    if not selected:
        selected = candidates[:max_items]

    recent_user = [
        m["content"]
        for m in messages
        if m.get("role") == "user" and m.get("content")
    ][-3:]

    if recent_user:
        selected.append("Recent user topics: " + " | ".join(recent_user))

    return "\n".join(selected)


def memory_stats():
    facts = load_facts()
    messages = load_messages()
    return {
        "messages": len(messages),
        "facts": len(facts.get("notes", [])),
        "preferences": len(facts.get("preferences", [])),
    }


def clear_all_memory():
    save_messages([])
    save_facts({})
    return True
