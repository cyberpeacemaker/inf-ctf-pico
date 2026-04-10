# Python Encode | Amazing

```python
# Replace 'encoded_string' with the actual garbled text from your CTF
encoded_string = "灩捯捴晦" 

# Use a list comprehension to unpack every character in the string
# chr(val >> 8) gets the first byte
# chr(val & 0xFF) gets the second byte
decoded_chars = [chr(ord(c) >> 8) + chr(ord(c) & 0xFF) for c in encoded_string]

# Join the pairs back into a single string
flag = "".join(decoded_chars)

print(f"Decoded Flag: {flag}")
```

# Python Encode | Insane

```python
# 'utf-16be' stands for UTF-16 Big Endian
encoded_string = "灩捯捴晦"
flag = encoded_string.encode('utf-16-be').decode('utf-8')
print(flag)
```

---

# shift operation C v.s Python
You’ve hit on one of the biggest differences between high-level languages like Python and low-level languages like C. The short answer: **Yes, they both use `<<`, but they handle the "container" very differently.**

### 1. C: The Fixed-Width Bucket
In C, variables have a fixed size in memory (e.g., an `unsigned char` is 8 bits, an `int` is usually 32 bits). 

When you shift bits in C, the "bucket" stays the same size. If you shift a bit past the edge of that bucket, it simply **falls off and is lost forever**.

* **Example:** If you have an 8-bit `char` with the value `10110011` and you shift it left by 1 (`<< 1`), the result is `01100110`. The leading `1` is gone.
* **Overflow:** If you try to shift an `int` too far, it doesn't get bigger; it just eventually becomes zero (or triggers undefined behavior if you're not careful).



---

### 2. Python: The Infinite Ribbon
Python integers are **arbitrary-precision**. They don't have a fixed size like 8, 32, or 64 bits. Instead, Python automatically allocates more memory as the number grows.

When you use `<<` in Python, the variable "stretches" to accommodate the new bits.

* **Example:** If you have the number `5` (`101` in binary) and you do `5 << 100`, Python will happily create a massive integer with 100 zeros at the end. It won't lose any data unless you run out of RAM.
* **Dynamic Change:** You aren't "changing the bits of the variable" in the sense of overwriting a specific memory address like in C; you are creating a new integer object that is mathematically larger.

---

### 3. Comparison Table

| Feature | C / C++ | Python |
| :--- | :--- | :--- |
| **Size** | Fixed (8, 16, 32, 64 bits) | Arbitrary (grows as needed) |
| **Overflow** | Bits are dropped (lost) | Variable expands (no data lost) |
| **Performance** | Extremely fast (direct CPU instruction) | Slower (handled by Python's runtime) |
| **Memory** | Pre-allocated and static | Dynamically allocated |
