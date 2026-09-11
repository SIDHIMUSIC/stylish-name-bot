"""Tiny JSON store for group chats that should get hourly promos."""
from __future__ import annotations

import json
import os
from pathlib import Path

DATA_PATH = Path(os.getenv("DATA_PATH", "data/chats.json"))


def _load() -> dict:
    if not DATA_PATH.exists():
        return {"groups": []}
    try:
        return json.loads(DATA_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"groups": []}


def _save(data: dict) -> None:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")


def add_group(chat_id: int) -> None:
    data = _load()
    groups = data.setdefault("groups", [])
    if chat_id not in groups:
        groups.append(chat_id)
        _save(data)


def remove_group(chat_id: int) -> None:
    data = _load()
    groups = data.setdefault("groups", [])
    if chat_id in groups:
        groups.remove(chat_id)
        _save(data)


def list_groups() -> list[int]:
    return list(_load().get("groups", []))
