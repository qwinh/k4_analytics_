import os
import re

folder = "texts"

# This regex matches any punctuation or number and replaces with space
# Then cleans up multiple spaces
def clean_text(text):
    # Step 1: Replace punctuation & numbers with space
    text = re.sub(r'[^\w\s]|[\d]', ' ', text)   # \w = letters, _ ; \s = space
    # Step 2: Replace multiple spaces (including tabs, newlines) with single space
    text = re.sub(r'\s+', ' ', text)
    # Step 3: Strip leading/trailing spaces
    return text.strip()

# Process every .txt file
for filename in os.listdir(folder):
    if filename.endswith(".txt"):
        filepath = os.path.join(folder, filename)
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        cleaned = clean_text(content.lower())  # .lower() optional but recommended
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(cleaned)
        
        print(f"Cleaned: {filename}")

print("All files cleaned: punctuation/numbers → space, multiple spaces → single space")