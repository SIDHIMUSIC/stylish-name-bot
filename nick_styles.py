def _combine(text, mark):
    return "".join((ch + mark) if ch.isalnum() else ch for ch in text)


def build_all(name):
    name = (name or "").strip()[:24] or "Name"
    up = name.upper()
    items = []
    T = [
        "\u2605\u00b8.\u2022\u00b4\u00af`\u2022.\u00b8\u2605 {n} \u2605\u00b8.\u2022\u00b4\u00af`\u2022.\u2605",
        ".\u2022\u266b\u2022\u266c\u2022 {n} \u2022\u266c\u2022\u266b\u2022.",
        "\u2570\u2606\u2606 {n} \u2606\u2606\u256e",
        "\u2661 {n} \u2661",
        "\u273f {n} \u273f",
        "\u2740 {n} \u2740",
        "\u2764\ufe0f {n} \U0001F47B \u00d7",
        "\u2022 {n} \u2764\ufe0f",
        "I'M \u2192 {n} \u2764\ufe0f \u00d7 \u2192",
        "i am.. \u2605\u2605\u2605 {n} \u2605",
        "\u00b0+ cute {n} \u00b0 \U0001F339",
        "\u265B {n} \u265B",
        "\U0001F451 {n} \U0001F451",
        "\u300E {n} \u300F",
        "\u300C {n} \u300D",
        "\u3010 {n} \u3011",
        "\u2620 {n} \u2620",
        "\u00d7\u035c\u00d7 {n} \u4e97",
        "\u26A1 {n} \u26A1",
        "\U0001F525 {n} \U0001F525",
        "{n} \u2665 you",
        "only {n} \U0001F497",
        "my {n} \U0001F49E",
        "{n} jaan",
        "me \u00d7 {n}",
        "raja {n}", "rani {n}", "jaanu {n}", "pagal {n}", "dil {n}",
        "babu {n}", "desi {n}", "{n} bhai", "{n} ji",
        "\u00d7\u035c\u00d7{n}", "\u4e97{n}", "\u2605{n}\u2605", "[{n}]", "OP{n}",
        "\u0d7d\u0f12 {n} \u0f12\u0d7e", "\u0f3a {n} \u0f3b",
        "\u2727\u0f3a {n} \u0f3b\u2727", "\ua4f0 {n} \ua4f1",
        "\u2661\u208a\u02da {n} \u02da\u208a\u2661", "\u22c6 {n} \u22c6",
        "\u2606 {n} \u2606", "\u271d {n} \u271d", "\u2020 {n} \u2020",
        "\u30c4 {n} \u30c4", "\u30b7 {n} \u30b7",
        "\u23af {n} \u23af", "\u2501 {n} \u2501", "\u2248 {n} \u2248", "\u221e {n} \u221e",
    ]
    for t in T:
        items.append(t.replace("{n}", name))
        items.append(t.replace("{n}", up))
    for mark in ["\u0336", "\u0332", "\u0331", "\u0305", "\u0338", "\u0324", "\u0362", "\u033d"]:
        c = _combine(name, mark)
        items.extend([c, f"\u2605 {c} \u2605", f"\u2661 {c} \u2661", f"\u26A1 {c}", f"\u3010{c}\u3011", f"\u00d7\u035c\u00d7 {c} \u4e97"])
    P = ["","\u2605 ","\u2606 ","\u2726 ","\u265B ","\U0001F451 ","\u2661 ","\u2764\ufe0f ","\U0001F338 ","\U0001F525 ","\u26A1 ","\u00d7\u035c\u00d7 ","\u4e97 ","\u30c4 ","\u300E ","\u300C ","\u3010 ","\u2022 ","I'M ","its ","Mr. ","miss ","baby ","only ","my ","king ","pro ","god ","pagal ","dil ","jaanu ","sona ","raja ","babu ","desi ","swag "]
    S = [""," \u2605"," \u2606"," \u2726"," \u265B"," \U0001F451"," \u2661"," \u2764\ufe0f"," \U0001F338"," \U0001F525"," \u26A1"," \u4e97"," \u30c4"," \u300F"," \u300D"," \u3011"," \u2022"," \u00d7"," \U0001F47B"," <3"," \u2713"," ji"," bhai"," jaan"," baby"," forever"]
    for i,p in enumerate(P):
        for j,s in enumerate(S):
            if (i+j)%2==0:
                items.append(f"{p}{name}{s}".strip())
            if j%5==0:
                items.append(f"{p}{up}{s}".strip())
            if j%7==0:
                items.append(f"{p}{_combine(name, chr(0x0332))}{s}".strip())
    if " " not in name and len(name)<=16:
        items += [" ".join(name), "\u00b7".join(name), "_".join(name), " ".join(up), _combine(" ".join(name), "\u0332")]
    out, seen = [], set()
    for x in items:
        x = " ".join(str(x).split())
        if x and x not in seen:
            seen.add(x); out.append(x)
    return out
