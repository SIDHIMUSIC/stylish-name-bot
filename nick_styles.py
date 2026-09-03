def build_all(name):
    name = (name or "").strip()[:28] or "Name"
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
        "raja {n}",
        "rani {n}",
        "jaanu {n}",
        "pagal {n}",
        "dil {n}",
        "babu {n}",
        "desi {n}",
        "{n} bhai",
        "{n} ji",
        "\u00d7\u035c\u00d7{n}",
        "\u4e97{n}",
        "\u2605{n}\u2605",
        "[{n}]",
        "OP{n}",
    ]
    P = ["","\u2605 ","\u2606 ","\u2726 ","\u265B ","\U0001F451 ","\u2661 ","\u2764\ufe0f ","\U0001F338 ","\U0001F525 ","\u26A1 ","\u00d7\u035c\u00d7 ","\u4e97 ","\u30c4 ","\u300E ","\u300C ","\u3010 ","\u2022 ","I'M ","its ","Mr. ","miss ","baby ","only ","my ","king ","pro ","god ","pagal ","dil ","jaanu ","sona ","raja ","babu ","desi ","swag "]
    S = [""," \u2605"," \u2606"," \u2726"," \u265B"," \U0001F451"," \u2661"," \u2764\ufe0f"," \U0001F338"," \U0001F525"," \u26A1"," \u4e97"," \u30c4"," \u300F"," \u300D"," \u3011"," \u2022"," \u00d7"," \U0001F47B"," <3"," \u2713"," ji"," bhai"," jaan"," baby"," forever"]
    out, seen = [], set()
    def add(x):
        x = " ".join(x.split())
        if x and x not in seen:
            seen.add(x); out.append(x)
    for t in T:
        add(t.replace("{n}", name))
    for i,p in enumerate(P):
        for j,s in enumerate(S):
            if (i+j)%2==0:
                add(f"{p}{name}{s}".strip())
    if " " not in name and len(name)<=16:
        add(" ".join(name)); add("\u00b7".join(name)); add("_".join(name))
    return out
