"""
This script generates a set of 160 unique, valid random device names. 
Names are biased toward shorter lengths and must meet specific formatting rules, as defined by IoT OD.
"""

import random
import string
import re

# Random name generator with skewed lengths
def generate_random_string():
    """
    Generate a random device name with more short-to-mid-length names than long ones.
    """
    rand = random.random()
    if rand < 0.7:
        length = random.randint(4, 12)
    elif rand < 0.95:
        length = random.randint(13, 25)
    else:
        length = random.randint(26, 50)
    
    valid_chars = string.ascii_letters + string.digits + '+-.'
    return ''.join(random.choices(valid_chars, k=length))

# Validation function
def valid(name):
    allowed_re = re.compile(r'^[a-z0-9\+\-\.]{3,50}$', re.IGNORECASE)
    return bool(allowed_re.match(name)) and any(c.isdigit() for c in name)

random.seed(160)
names = set()

while len(names) < 160:
    n = generate_random_string()
    if valid(n):
        names.add(n)

output_text = "\n".join(sorted(names))
print(output_text)
