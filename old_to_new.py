import re
import os
from pathlib import Path

def fix_text(sample: str) -> str:
    pattern = (
        r'[bcdđghklmnprstvx][aoôơuư][ìỉĩíị]\b|\b[aoôơuư][ìỉĩíị]\b'
        r'|[ae][òỏõóọ]\b|[aâêiyươ][ùũủúụ]\b|[aâ][ỳỷỹýỵ]\b'
        r'|[aâ][ỳỷỹýỵ]\b|[ae][òỏõóọ]\b'
        r'|[bcdđhklmnprstvx][aâêiyươ][ùũủúụ]\b|\b[aâêiyươ][ùũủúụ]\b'
        r'|[òỏõóọ][aăeo]|[ùũủúụ]yê|[ùũủúụ][âêyơô]|[ìỉĩíịỳỷỹýỵ]ê|[ừửữứự]ơ'
        r'|g[ìỉĩíị][aăeêoôơuư]|q[ùũủúụ][ai]'
    )
    
    sets = [
        'aăâeêioôơuưy',
        'àằầèềìòồờùừỳ',
        'ảẳẩẻểỉỏổởủửỷ',
        'ãẵẫẽễĩõỗỡũữỹ',
        'áắấéếíóốớúứý',
        'ạặậẹệịọộợụựỵ'
    ]
    
    found = re.findall(rf'\b\w*?({pattern})\w*?\b', sample, re.IGNORECASE)
    replacing = {}
    
    for combination in found:
        tone, toned_char, toned_char_index = 0, '', 0
        consonant = '' if not re.match(r'^[bcdđghklmnpqrstvx].*', combination, re.IGNORECASE) else combination[0].lower()
        
        for i in range(1, 6):
            if (char := re.search(rf"[{sets[i]}]", combination, re.IGNORECASE)):
                toned_char = char[0]
                toned_char_index = sets[i].index(toned_char.lower())
                tone = i
                break
        
        position_ = combination.index(toned_char)
        position = position_ - 1
        if consonant in ['g', 'q']:
            position = position_ + 1

        position_ = combination.index(toned_char)
        position = position_ - 1
        if consonant in ['g', 'q']:
            position = position_ + 1

        # ←←← MINIMAL SAFETY FIX (prevents ALL out-of-range crashes) ←←←
        if position < 0:
            position = position_ + 1
        elif position >= len(combination):
            position = max(0, position_ - 1)
        # ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←

        nuclear = combination[position]

        nuclear = combination[position]
        
        nuclear_index = sets[0].index(nuclear.lower())
        new_combination = sets[0][toned_char_index] + sets[tone][nuclear_index]
        if len(combination) > 2 and consonant == '':
            new_combination = sets[0][toned_char_index] + combination[1] + sets[tone][nuclear_index]
        if position == 0 or (len(combination) > 2 and consonant not in ['', 'g', 'q']):
            new_combination = new_combination[::-1]
        new_combination = consonant + new_combination
        
        if combination.isupper():
            new_combination = new_combination.upper()
        elif combination[0].isupper():
            new_combination = new_combination.capitalize()
        replacing[combination] = new_combination
    
    for original, corrected in replacing.items():
        if not re.match(r'^([iu][àảãáạ]|u[ìỉĩíị])$', original, re.IGNORECASE):
            sample = re.sub(rf"\b(\w*?){re.escape(original)}(\w*?)\b", rf"\1{corrected}\2", sample)
        else:
            sample = re.sub(rf"\b{re.escape(original)}\b", corrected, sample)
    
    return sample

old_dir = Path("old")
out_dir = Path("texts")
out_dir.mkdir(exist_ok=True)

for txt_file in old_dir.glob("*.txt"):
    text = txt_file.read_text(encoding="utf-8")
    fixed = fix_text(text)
    (out_dir / txt_file.name).write_text(fixed, encoding="utf-8")
    print(f"Fixed: {txt_file.name}")

print("All done!")