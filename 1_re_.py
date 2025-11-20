# re_fixed_and_final.py
import os
import unicodedata

MAPS_FILE = "maps_flipped.txt"
INPUT_FILE = "text.txt"

print("Current folder:", os.getcwd())
print("Maps file     :", os.path.abspath(MAPS_FILE))
print("Input file    :", os.path.abspath(INPUT_FILE))
print("-" * 60)

def clean_key(s):
    """Remove every kind of invisible garbage that breaks dict lookup"""
    s = s.replace("\ufeff", "")       # BOM
    s = s.replace("\u200b", "")       # zero-width space
    s = s.replace("\u2060", "")       # word joiner
    s = s.replace("\u00a0", " ")      # non-breaking space
    s = s.strip(" \t\r\n\u2028\u2029")
    return unicodedata.normalize("NFC", s)

# Load mapping with aggressive cleaning
mapping = {}
with open(MAPS_FILE, "r", encoding="utf-8") as f:
    for line_num, line in enumerate(f, 1):
        line = line.rstrip("\n\r")
        if not line or "\t" not in line:
            continue
        vi_raw, k4 = line.split("\t", 1)
        vi = clean_key(vi_raw)
        k4 = k4.strip()
        if vi in mapping:
            print(f"Duplicate key ignored (line {line_num}): {vi!r}")
        else:
            mapping[vi] = k4

print(f"Loaded {len(mapping):,} unique entries")
print()

# Show proof that the keys are really there (with hex dump)
print("Sample keys containing important words (hex dump):")
with open(MAPS_FILE, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i > 200:
            break
        if any(word in line for word in ["người", "trời", "trăm", "năm", "ngẫm", "muôn"]):
            key = line.split("\t", 1)[0]
            print(f"  {key!r}")
            print("    hex:", " ".join(f"{ord(c):04X}" for c in key))

print("\nTesting your sentence:")
sentence = "một cửa để bia muôn đời ngẫm hay muôn sự tại trời trời kia đã bắt làm người có thân"
for word in sentence.split():
    cleaned = clean_key(word)
    if cleaned in mapping:
        print(f"  {word!r} -> {cleaned!r} ==> {mapping[cleaned]}")
    else:
        print(f"  {word!r} -> {cleaned!r} NOT FOUND")

# Actual conversion
output_file = INPUT_FILE.replace(".txt", "_k4.txt")
with open(INPUT_FILE, "r", encoding="utf-8") as fin, open(output_file, "w", encoding="utf-8") as fout:
    for line in fin:
        words = line.split()
        out = []
        for w in words:
            head = tail = ""
            tmp = w
            while tmp and tmp[0] in "([{'\"":
                head += tmp[0]
                tmp = tmp[1:]
            while tmp and tmp[-1] in ".,!?;:'\")]}":
                tail = tmp[-1] + tail
                tmp = tmp[:-1]
            cleaned = clean_key(tmp)
            replacement = mapping.get(cleaned, tmp)
            out.append(head + replacement + tail)
        fout.write(" ".join(out) + "\n")

print(f"\nDONE! Converted file saved as: {output_file}")