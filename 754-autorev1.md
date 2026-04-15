

# hexadecimal | decimal

### 1. The Data Type Issue
In Python 3, `pwntools` generally prefers **bytes** over strings. While it sometimes handles strings automatically, it is safest to send bytes. 
* **Current:** `io.sendline(hex_val)` (Sends the string representation)
* **Best Practice:** `io.sendline(hex_val.encode())`

### 2. Hex vs. Decimal (The "Logic" Trap)
This is the most common reason scripts fail on this specific picoCTF challenge. 
* Your regex `movl $0x..., -0x4(%rbp)` finds a **hexadecimal** value (e.g., `0x539`).
* If the server asks "What's the secret?", it usually expects the **decimal** version of that number (e.g., `1337`).

If you send `hex_val` directly, you are sending the string "539". If the server expects "1337", your script will pass the technical check but fail the challenge logic.

### Why your previous error happened
The `TypeError: 'int' object is not iterable` occurred because `pwntools` tried to "pack" your integer. In its internal code, it tries to check every character in your input to see if it's a valid byte. Since an integer (like `1337`) isn't a collection of characters, it crashed.

### Quick Debugging Tip
Add a print statement before you send the data so you can see what your script is "thinking":
`print(f"Extracted hex: {hex_val} | Sending decimal: {secret_int}")`
```python
if match:
    hex_val = match.group(1)
    # Convert hex string to integer
    secret_int = int(hex_val, 16) 
    # Convert integer to string and send as bytes
    io.sendline(str(secret_int).encode())
```


# 64bit ELF | 7f454c46

```python
from pwn import *
import subprocess
import os
import re

# Connect to the challenge
io = remote('mysterious-sea.picoctf.net', 56082)

# Skip the intro text
io.recvuntil(b'Good luck >:)\n')
session_id = io.recvline() # This captures the "423429422"

for i in range(20):
    print(f"Solving Binary #{i+1}")
    
    # 1. Parse the hex bytes
    io.recvuntil(b'bytes:\n')
    hex_data = io.recvuntil(b'\nWhat\'s the secret?:', drop=True).decode()
    
    # 2. Convert hex to binary file
    binary_bytes = bytes.fromhex(hex_data)
    with open("temp_bin", "wb") as f:
        f.write(binary_bytes)
    os.chmod("temp_bin", 0o755) # Make it executable

    # 3. Extract the secret (Strategy: strings)
    # Example: If the secret looks like a specific format or is the last string
    # Change this logic based on what 'strings temp_bin' actually reveals
    # result = subprocess.check_output("strings temp_bin | grep 'some_pattern'", shell=True).strip()
    output = subprocess.check_output(["objdump", "-d", "temp_bin"]).decode()
    match = re.search(r'movl\s+\$0x([0-9a-fA-F]+),-0x4\(%rbp\)', output)

    if match:
        hex_val = match.group(1)
        # Convert hex string to integer
        secret_int = int(hex_val, 16) 
        # Convert integer to string and send as bytes
        io.sendline(str(secret_int).encode())

# Get the flag
io.interactive()
```