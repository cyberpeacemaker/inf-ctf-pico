
# CTF expected input format
When you look at assembly code through `objdump`, you are seeing the raw machine instructions represented in **hexadecimal** (base-16). However, when a program asks for input via `scanf` or `cin`, it usually expects **decimal** (base-10) unless the programmer specifically coded it to read hex.

Here is the breakdown of that "Logic Trap":

### 1. What the Assembly Sees
In your `objdump` output, you might see a line like this:
`movl   $0x3039,-0x4(%rbp)`

The `0x3039` is a hexadecimal value. To the computer's CPU, this is just a sequence of bits: `0011 0000 0011 1001`.

### 2. What your Regex Captures
Your current regex `match.group(1)` pulls the string **"3039"**. 
If you use `io.sendline(hex_val)`, you are sending the ASCII characters **'3', '0', '3', '9'** over the wire.

### 3. What the Program Expects
The target binary is likely running code that looks like this:
```c
int secret = 12345; // 12345 in decimal is 0x3039 in hex
int user_input;
scanf("%d", &user_input); // %d expects decimal!
if (user_input == secret) { ... }
```

If the program uses `%d`, it is waiting for the characters **'1', '2', '3', '4', '5'**. 
* If you send **"3039"**, the program reads it as the number three-thousand-and-thirty-nine.
* Since $3039 \neq 12345$, the program tells you the secret is wrong.

### The Conversion Logic
To bridge this gap, you have to perform a "Type Round-Trip" in your script:

| Step | Data | Type |
| :--- | :--- | :--- |
| **Capture** | `"3039"` | String (Hex) |
| **Convert** | `int("3039", 16)` $\rightarrow$ `12345` | Integer |
| **Format** | `str(12345)` $\rightarrow$ `"12345"` | String (Decimal) |
| **Send** | `io.sendline(b"12345")` | Bytes |

---

### How to verify this
Before you run the script, do a manual test:
1. Run the challenge once manually.
2. Copy the hex bytes it gives you.
3. Save them to a file: `echo "HEX_BYTES_HERE" | xxd -r -p > test_bin`.
4. Run `objdump -d test_bin` and find the `movl` value (e.g., `0xabc`).
5. Convert `abc` to decimal using a calculator (e.g., `2748`).
6. Type `2748` into the challenge prompt.

If `2748` works but `abc` doesn't, you know for certain your script must convert to decimal before sending.

Does the challenge give you any hint about the input format, like "Enter the number:", or does it just say "What's the secret?"

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
```python
# Converts hex string directly to bytes, then to an integer
raw_bytes = bytes.fromhex(hex_val.strip('0x'))
secret_int = int.from_bytes(raw_bytes, byteorder='big')
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