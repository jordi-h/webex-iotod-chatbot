"""
This script reads lines from 'test.txt' and replaces placeholders of the form {X|devicename}
with device names from a plaintext file.
"""

with open("test.txt", "r") as entries_file:
    entries = entries_file.readlines()

with open("test_realistic_names.txt", "r") as names_file:
    names = names_file.readlines()

# Clean newline characters
entries = [line.strip() for line in entries]
names = [name.strip() for name in names]

# Replace only the X inside {X|devicename}
import re

pattern = r"\{(X)\|devicename\}"

output_lines = [
    re.sub(pattern, f"{{{name}|devicename}}", line)
    for line, name in zip(entries, names)
]

# Save to a new file (optional)
with open("output.txt", "w") as output_file:
    for line in output_lines:
        output_file.write(line + "\n")

print("Replacement done.")
