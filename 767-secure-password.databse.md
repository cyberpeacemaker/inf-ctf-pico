
# charcode, hex

# bleed

# djb2

# assemble basic | while loop
Good eye—those two jumps are what *create the loop structure*. Let’s break them down clearly.

---

## 🔁 The two jumps

### 1. `131d: jmp 133d`

This is an **unconditional jump**.

👉 It skips over the hash computation on the first pass and goes straight to:

```asm
133d:   ; load next character
```

### Why?

Because this function is structured like a **`while` loop**, not a `do-while`.

Equivalent idea:

```c
while (condition) {
    body;
}
```

So it:

1. Jumps to check/load the condition first
2. Then executes the body only if needed

---

### 2. `1356: jne 131f`

This is a **conditional jump** (`jne = jump if not equal to zero`).

It comes after:

```asm
1352: cmpl $0x0, -0xc(%rbp)
```

So it means:

👉 **If current character ≠ 0 (`'\0'`), jump back to the loop body**

---

## 🧠 Putting it together (control flow)

### Flow looks like this:

```text
        jmp 133d        ; go check first char

LOOP_BODY (131f):
        hash = hash * 33 + c

CHECK (133d):
        c = *str++
        if (c != 0)
            jump to LOOP_BODY
        else
            exit
```

---

## 🔄 Equivalent C structure

```c
hash = 5381;

c = *str++;
while (c != 0) {
    hash = hash * 33 + c;
    c = *str++;
}
```

---

## ⚖️ Why both are needed

* `jmp 133d` → ensures **condition is checked before first iteration**
* `jne 131f` → controls **loop continuation**

If the first `jmp` wasn’t there, it would behave like:

```c
do {
    ...
} while (...);
```

—which would process at least one character even if it's `'\0'`.

---

## ✅ Summary

* `jmp 133d` → jump forward to start loop condition (setup `while`)
* `jne 131f` → jump back if condition true (loop continues)

Together they implement a clean **pre-check loop (while loop)** instead of a do-while.

---

If you want, I can redraw this as a control-flow graph (CFG)—that’s super helpful for reversing.
