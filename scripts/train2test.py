"""
Train/test splits creation.
This script randomly selects a given number of lines from 'train.txt', moves them to 'test.txt',
and removes them from the original file.
#! Note: This script must be placed in the same directory as 'train.txt' and 'test.txt', meaning inside the specific domain folder.
"""

import random

# File paths
input_file = 'train.txt'
output_file = 'test.txt'

# Number of lines to pick
num_samples = 160

# Read all lines from the input file
with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Sample lines
sampled_lines = random.sample(lines, min(num_samples, len(lines)))

# Write sampled lines to test.txt
with open(output_file, 'w', encoding='utf-8') as f:
    f.writelines(sampled_lines)

# Remove sampled lines (only the same number of times they appear)
remaining_lines = lines[:]
for line in sampled_lines:
    if line in remaining_lines:
        remaining_lines.remove(line)

# Write remaining lines back to train.txt
with open(input_file, 'w', encoding='utf-8') as f:
    f.writelines(remaining_lines)

print(f'{len(sampled_lines)} lines moved to {output_file} and removed from {input_file}')
