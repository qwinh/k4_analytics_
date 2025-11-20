# flip_map.py
import unicodedata
import sys

INPUT = "maps.txt"      # change this if your file has different name
OUTPUT = "maps_flipped.txt"

# Optional: force everything to NFC (recommended for final use)
NORMALIZE_TO_NFC = True

with open(INPUT, "r", encoding="utf-8") as fin, \
     open(OUTPUT, "w", encoding="utf-8") as fout:

    for line_num, line in enumerate(fin, 1):
        line = line.rstrip("\n\r")
        if not line or line.startswith("#"):
            fout.write(line + "\n")
            continue

        # Split on whitespace OR tab
        parts = line.split(None, 1)        # splits on any whitespace, keeps the rest
        if len(parts) != 2:
            print(f"Skipping bad line {line_num}: {line!r}")
            continue

        k4_key, viet_word = parts

        if NORMALIZE_TO_NFC:
            viet_word = unicodedata.normalize("NFC", viet_word)

        fout.write(f"{viet_word}\t{k4_key}\n")

print(f"Done! Flipped map saved as → {OUTPUT}")
print(f"   Total lines processed: {line_num}")