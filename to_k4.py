import os
import unicodedata
from pathlib import Path

# ========================= CONFIG =========================
MAPS_FILE = "maps_flipped.txt"        # Your Vietnamese → K4 mapping file
INPUT_FOLDER = "texts"                # Input folder
OUTPUT_FOLDER = "texts_k4"            # Output folder
# =========================================================

def clean_key(s: str) -> str:
    """Aggressively clean strings for reliable dictionary lookup"""
    s = s.replace("\ufeff", "")       # BOM
    s = s.replace("\u200b", "")       # zero-width space
    s = s.replace("\u2060", "")       # word joiner
    s = s.replace("\u00a0", " ")      # non-breaking space → normal space
    s = s.strip(" \t\r\n\u2028\u2029")
    return unicodedata.normalize("NFC", s)


def load_mapping(maps_path: Path):
    """Load the tab-separated mapping file with duplicate protection"""
    mapping = {}
    if not maps_path.exists():
        raise FileNotFoundError(f"Mapping file not found: {maps_path}")

    with open(maps_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.rstrip("\n\r")
            if not line or "\t" not in line:
                continue
            vi_raw, k4 = line.split("\t", 1)
            vi = clean_key(vi_raw)
            k4 = k4.strip()

            if vi in mapping:
                print(f"Warning: Duplicate key ignored (line {line_num}): {vi!r}")
            else:
                mapping[vi] = k4

    print(f"Loaded {len(mapping):,} unique entries from {maps_path.name}")
    return mapping


def convert_text(text: str, mapping: dict) -> str:
    """Convert a single line preserving punctuation and brackets"""
    words = text.split()
    out = []
    for w in words:
        head = tail = ""
        tmp = w

        # Extract leading punctuation/brackets
        while tmp and tmp[0] in "([{'\"":
            head += tmp[0]
            tmp = tmp[1:]

        # Extract trailing punctuation/brackets
        while tmp and tmp[-1] in ".,!?;:'\")]}":
            tail = tmp[-1] + tail
            tmp = tmp[:-1]

        cleaned = clean_key(tmp)
        replacement = mapping.get(cleaned, tmp)  # fallback to original if not found
        out.append(head + replacement + tail)

    return " ".join(out)


def process_all_files():
    maps_path = Path(MAPS_FILE)
    input_folder = Path(INPUT_FOLDER)
    output_folder = Path(OUTPUT_FOLDER)

    print("Vietnamese → K4 Batch Converter")
    print("=" * 60)
    print(f"Mapping file : {maps_path.resolve()}")
    print(f"Input folder : {input_folder.resolve()}")
    print(f"Output folder: {output_folder.resolve()}")
    print("-" * 60)

    # Load mapping once
    mapping = load_mapping(maps_path)

    # Create output directory
    output_folder.mkdir(parents=True, exist_ok=True)

    if not input_folder.exists():
        print(f"Error: Input folder '{INPUT_FOLDER}' does not exist!")
        return

    txt_files = list(input_folder.rglob("*.txt"))
    if not txt_files:
        print(f"No .txt files found in '{INPUT_FOLDER}'")
        return

    print(f"Found {len(txt_files)} file(s) to process...\n")

    success_count = 0
    for file_path in txt_files:
        try:
            relative = file_path.relative_to(input_folder)
            output_file = output_folder / relative.with_name(relative.stem + "_k4.txt")

            # Ensure subdirectories exist
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, 'r', encoding='utf-8') as fin:
                lines = fin.readlines()

            converted_lines = [convert_text(line.rstrip("\n\r"), mapping) + "\n" for line in lines]

            with open(output_file, 'w', encoding='utf-8') as fout:
                fout.writelines(converted_lines)

            print(f"Success: {relative} → {Path(OUTPUT_FOLDER) / relative.with_name(relative.stem + '_k4.txt')}")
            success_count += 1

        except Exception as e:
            print(f"Failed: {file_path} → Error: {e}")

    print("\n" + "="*60)
    print(f"Conversion complete! {success_count}/{len(txt_files)} files processed.")
    print(f"Results saved in: {output_folder.resolve()}")


if __name__ == "__main__":
    process_all_files()