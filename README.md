# Ec2b
A simple library, written in pure Python, to generate xorpad.

it's based on [GrownNed/ec2b.py](https://github.com/GrownNed/ec2b.py)

## Usage
```py
import ec2b
from base64 import b64encode

with open("Ec2bSeed.bin", "rb") as f:
    seed = f.read()

xor_pad = ec2b.derive(seed)

print(b64encode(xor_pad).decode())
```
