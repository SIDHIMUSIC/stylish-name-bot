"""Reusable frames copied from https://t.me/NAME_BOTGEN (not other users' names)."""

# Keep combining-mark flood LOW. These are the repeating wrappers from that channel.
FORMATS = [
    "\U000131a9 {n} \U000131aa",
    "\U000131a9{n}\U000131aa",
    "~ {n} ~",
    "\u268a {n} \u26a1",
    "\u4e5b \" {n} \U0001F497",
    "\u275d {n} \U0001F338 \u275e",
    "\u2018. {n}",
    "\u2500 {n} \U000131a9 \U0001F90D \U000131aa",
    "\u27f6 {n} \U0001F940",
    "\u27f5 {n} \U0001F494",
    "\u2726 {n} \u2726",
    "\u2765 {n} \u2765",
    "\u300e {n} \u300f",
    "\u3010 {n} \u3011",
    "\ua9c1 {n} \ua9c2",
    "{n} \U0001F525",
    "VIP {n}",
    "only {n}",
    "{n} jaan",
    "raja {n}",
]

def apply_formats(name: str) -> list[str]:
    n = (name or "Name").strip()[:24] or "Name"
    spaced = " ".join(n.upper())
    out = []
    for fmt in FORMATS:
        out.append(fmt.replace("{n}", n))
        out.append(fmt.replace("{n}", spaced))
    return out
