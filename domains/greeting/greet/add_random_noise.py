"""
This script injects random noise into lines from a text file (e.g., 'test.txt') 
by adding random alphanumeric characters outside protected {...} regions.
"""

import random
import string

def add_noise(text, noise_level=0.1):
    """
    Adds random characters to a string, excluding curly brackets {}.
    
    Parameters:
        text (str): The original text.
        noise_level (float): Proportion of the number of characters to insert relative to the text length.
                             For example, 0.1 adds ~10% noise.

    Returns:
        str: The noisy version of the text.
    """
    noisy_text = list(text)
    num_noise = max(1, int(len(text) * noise_level)) if text else 0

    # Create noise character pool without '{' and '}'
    noise_chars = string.ascii_letters + string.digits + ''.join(
        c for c in string.punctuation if c not in '{}'
    )

    for _ in range(num_noise):
        insert_char = random.choice(noise_chars)
        insert_pos = random.randint(0, len(noisy_text))
        noisy_text.insert(insert_pos, insert_char)

    return ''.join(noisy_text)

def process_file(input_path, output_path, noise_level=0.1):
    """
    Reads a file line by line, adds noise, and writes the result to a new file.

    Parameters:
        input_path (str): Path to the input file.
        output_path (str): Path to the output file.
        noise_level (float): Noise level per phrase.
    """
    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            clean_line = line.strip()
            if clean_line:
                noisy = add_noise(clean_line, noise_level=noise_level)
                outfile.write(noisy + '\n')
            else:
                outfile.write('\n')  # preserve empty lines if any

# Example usage
if __name__ == "__main__":
    # Change these paths as needed
    input_file = "test.txt"
    output_file = "test_noisy.txt"
    
    # Set noise level (e.g., 0.1 = 10% extra random characters)
    noise_proportion = 0.05
    
    process_file(input_file, output_file, noise_level=noise_proportion)
