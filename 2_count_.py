#!/usr/bin/env python3
# counts.py — ULTRA CLEAN, exactly what you asked for

import sys
from collections import Counter

if __name__ != "__main__":
    sys.exit()
sys.dont_write_bytecode = True

input_file = "text_k4.txt"
output_file = "k4_counts.txt"

try:
    text = open(input_file, "r", encoding="utf-8").read()
except FileNotFoundError:
    print("No text_k4.txt found")
    sys.exit(1)

freq = Counter(text)
total = len(text)

# B split
b = freq["B"] + freq["b"]
half_b = b / 2.0

# Groups
groups = {
    "Q + A":                   "QA",
    "W + S + Z":               "WSZ",
    "E + D + X":               "EDX",
    "R + F + C + G + V + ½B":  "RFCGVB",
    "H + N + U + J + M + ½B":  "HNUJMB",
    "I + K + ,":               "IK,",
    "O + L + .":               "OL.",
    "P + T":                   "PT"
}

with open(output_file, "w", encoding="utf-8") as f:
    f.write(f"Total chars: {total:,}\n\n")

    # Individual chars
    for ch, cnt in sorted(freq.items(), key=lambda x: (-x[1], x[0])):
        if ch == " ": ch = "<space>"
        elif ch == "\n": ch = "<newline>"
        elif not ch.isprintable(): ch = f"\\u{ord(ch):04x}"
        f.write(f"{ch}: {cnt}  ({cnt/total*100:.2f}%)\n")
    f.write("\n")

    # GROUPS — EXACTLY YOUR FORMAT
    for name, letters in groups.items():
        nums = []
        sum_group = 0.0
        for ch in letters:
            if ch == "B":
                count = half_b
            else:
                count = freq.get(ch, 0) + freq.get(ch.lower(), 0)
            nums.append(str(int(count)) if count == int(count) else f"{count:.1f}")
            sum_group += count
        total_int = int(sum_group) if sum_group == int(sum_group) else round(sum_group, 2)
        perc = sum_group / total * 100
        f.write(f"{name} = {total_int} ({perc:.2f}%)\n")
        f.write(f"{' '.join(nums)}\n\n")

print(f"Done → {output_file}")