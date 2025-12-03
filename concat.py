import os

# Folder containing your text files
folder = "texts_k4"

# Output file (will be created in the same directory as the script)
output_file = "k4.txt"

# Open the output file in write mode
with open(output_file, "w", encoding="utf-8") as outfile:
    # Go through all files in the folder
    for filename in sorted(os.listdir(folder)):          # sorted() makes it predictable
        if filename.endswith(".txt"):                     # only .txt files
            filepath = os.path.join(folder, filename)
            print(f"Adding: {filename}")                  # optional: show progress
            with open(filepath, "r", encoding="utf-8") as infile:
                outfile.write(infile.read())
                outfile.write("\n\n")                     # add blank line between files (optional)

print(f"\nDone! All files combined into {output_file}")