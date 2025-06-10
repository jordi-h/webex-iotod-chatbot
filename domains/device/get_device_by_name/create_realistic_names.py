"""
This script generates 160 unique, realistic-looking device names using a combination 
of codename-style words, device-related keywords, digits, abbreviations, and special characters.
"""

import random, re

# Base words
device_words = [
    "router", "rtr", "switch", "swt", "gateway", "gw", "edge", "core", "dist",
    "access", "uplink", "bridge", "node", "fabric", "fw", "vpn", "proxy", "mux",
    "ap", "agg"
]

codename_words = [
    "apollo", "athena", "zephyr", "helios", "atlas", "orion", "phoenix", "mercury",
    "nebula", "sirius", "vega", "capella", "talos", "odyssey", "sparta", "geneva",
    "oslo", "zurich", "dakota", "yukon", "rhine", "thames", "severn", "tiber",
    "nile", "volga", "elba", "arctic", "baltic", "cassini", "diode", "pixel",
    "quartz", "radon", "silica", "tango", "utopia", "valkyrie", "white", "xenon",
    "yara", "zenith", "argo", "bravo", "cobalt", "draco", "ember", "fargo",
    "gamma", "helium", "indigo", "jupiter", "krypton", "lithium", "mirage",
    "nomad", "onyx", "pegasus", "quest", "rio", "terra", "vortex", "wander",
    "wraith", "wrath", "xeros", "iron", "mesa", "oasis", "plasma", "sage",
    "theta", "ultra", "omega", "nova", "delta", "hydra", "raven", "fusion",
    "gladius", "ocean", "sigma", "wanderer"
]

special_chars = ['+', '-', '.']
suffixes = ['v1', 'v2', 'v3', 'us', 'eu', 'uk', 'apac', 'na', 'emea']

abbreviations = {
    "gateway": "gtw",
    "uplink": "uplk",
    "switch": "swt",
    "router": "rtr",
    "fabric": "fbr",
    "access": "acc",
    "bridge": "brdg"
}

def rand_digits():
    length = random.choice([1, 2, 3, 4])
    return ''.join(random.choices('0123456789', k=length))

def apply_abbreviation(word):
    if word in abbreviations and random.random() < 0.3:
        return abbreviations[word]
    return word

def insert_digit_randomly(word):
    if len(word) > 2 and random.random() < 0.2:
        pos = random.randint(1, len(word) - 1)
        return word[:pos] + str(random.randint(0, 9)) + word[pos:]
    return word

def random_case(name):
    if random.random() < 0.3:  # 30% of names get mixed casing
        return ''.join(c.upper() if random.random() < 0.5 else c for c in name)
    return name

def create_name():
    if random.random() < 0.1:
        # 10% simple very short names
        device = apply_abbreviation(random.choice(device_words))
        device = insert_digit_randomly(device)
        name = device + rand_digits()
    else:
        parts = []

        device = apply_abbreviation(random.choice(device_words))
        codename = random.choice(codename_words)
        codename2 = random.choice([c for c in codename_words if c != codename])
        device2 = apply_abbreviation(random.choice([d for d in device_words if d != device]))

        device = insert_digit_randomly(device)
        codename = insert_digit_randomly(codename)
        codename2 = insert_digit_randomly(codename2)
        device2 = insert_digit_randomly(device2)

        structure_type = random.choice(["simple", "complex", "double", "digits_heavy"])

        if structure_type == "simple":
            parts.append(random.choice([device, codename]))

        elif structure_type == "complex":
            parts.extend([device, codename])
            if random.random() < 0.5:
                parts.append(rand_digits())

        elif structure_type == "double":
            parts.extend([codename, device2, codename2])
            if random.random() < 0.7:
                parts.append(rand_digits())

        elif structure_type == "digits_heavy":
            parts.extend([rand_digits(), device, codename])
            if random.random() < 0.5:
                parts.append(rand_digits())

        name = parts[0]
        for part in parts[1:]:
            if random.random() < 0.4:  # 40% chance of inserting special char
                separator = random.choice(special_chars)
            else:
                separator = ''
            name += separator + part

        # Occasionally add a suffix
        if random.random() < 0.2:
            name += random.choice(['-', '.']) + random.choice(suffixes)

    return random_case(name.lower())

def valid(name):
    allowed_re = re.compile(r'^[a-z0-9\+\-\.]{3,50}$', re.IGNORECASE)
    return bool(allowed_re.match(name)) and any(c.isdigit() for c in name)

# Main generator
random.seed(160)
names = set()
while len(names) < 160:
    n = create_name()
    if valid(n):
        names.add(n)

output_text = "\n".join(sorted(names))
print(output_text)
