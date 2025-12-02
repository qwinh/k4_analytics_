import unicodedata
import os
from pathlib import Path

def to_telex(char):
    """
    Convert a single Vietnamese Unicode character to its Telex equivalent.
    Handles both lowercase and uppercase.
    Non-Vietnamese characters are returned as-is.
    """
    is_upper = char.isupper()
    char_lower = char.lower()
    
    if char_lower == 'đ':
        return 'Dd' if is_upper else 'dd'
    
    decomp = unicodedata.normalize('NFD', char_lower)
    parts = list(decomp)
    
    if len(parts) == 1:
        result = parts[0]
    else:
        base = parts[0]
        diac = ''
        tone = ''
        for p in parts[1:]:
            code = ord(p)
            if code == 0x0302:      # circumflex ^
                if base in 'aeo':
                    diac = 'a' if base == 'a' else 'e' if base == 'e' else 'o'
            elif code == 0x0306:    # breve
                diac = 'w'
            elif code == 0x031B:    # horn
                diac = 'w'
            elif code == 0x0301:   # acute ´
                tone = 's'
            elif code == 0x0300:    # grave `
                tone = 'f'
            elif code == 0x0309:    # hook above
                tone = 'r'
            elif code == 0x0303:    # tilde ~
                tone = 'x'
            elif code == 0x0323:    # dot below
                tone = 'j'
        
        result = base + diac + tone
    
    # Preserve capitalization
    if is_upper and result:
        result = result[0].upper() + result[1:]
    
    return result


def viet_to_telex(text: str) -> str:
    """
    Convert a full Vietnamese text string to its Telex equivalent.
    """
    converted = ''.join(to_telex(c) for c in text)
    # Common post-processing: "uw" → "w" (ư, ơ cases)
    return converted.replace("uw", "w")


def process_folder(input_folder: str = "texts", output_folder: str = "texts_telex"):
    """
    Convert all .txt files from input_folder to Telex and save them in output_folder.
    """
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    
    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    
    if not input_path.exists():
        print(f"Error: Input folder '{input_folder}' not found!")
        return
    
    txt_files = list(input_path.rglob("*.txt"))  # also catches files in subfolders
    
    if not txt_files:
        print(f"No .txt files found in '{input_folder}'")
        return
    
    print(f"Found {len(txt_files)} .txt file(s). Starting conversion...\n")
    
    for file_path in txt_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            telex_content = viet_to_telex(content)
            
            # Build output filename: keep relative path inside output folder
            relative = file_path.relative_to(input_path)
            output_file = output_path / relative.with_name(relative.stem + "_telex.txt")
            
            # Ensure subdirectories exist in output folder
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(telex_content)
            
            print(f"Success: {file_path} → {output_file}")
        
        except Exception as e:
            print(f"Failed: {file_path} → Error: {e}")
    
    print("\nAll done!")


if __name__ == "__main__":
    process_folder("texts", "texts_telex")