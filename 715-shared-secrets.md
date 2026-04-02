
# diffie hellman

To decrypt the flag, you are essentially reversing a **Stream Cipher** where the "key" is a single byte derived from the Diffie-Hellman exchange.

In your `encryption.py` script, the encryption was done like this:
`enc = bytes([x ^ (shared % 256) for x in flag])`

Here is exactly how to "un-XOR" that string to get your flag.

---

## 1. The Math of XOR (`^`)
The XOR (Exclusive OR) operation has a unique property: it is its own inverse. 
* If $A \oplus B = C$, then $C \oplus B = A$.
* In your case: $\text{Plaintext Byte} \oplus \text{Key} = \text{Ciphertext Byte}$.
* Therefore: $\text{Ciphertext Byte} \oplus \text{Key} = \text{Plaintext Byte}$.

Because the script used `shared % 256`, it took the massive `shared` number and "chopped off" everything except the very last byte (since $256 = 2^8$, or one byte).

---

## 2. Why `shared % 256`?
The `shared` secret you calculated ($A^b \pmod{p}$) is a gargantuan number with hundreds of digits. However, a single character in a string (like 'p' in `picoCTF`) is only 8 bits (1 byte). 

By using the modulo operator `% 256`, the script ensures the key is a value between **0 and 255**, which fits perfectly into a single byte for the XOR operation.



---

## 3. Step-by-Step Decryption Script
Now that you have $p$, $A$, and $b$ (from your `file.txt`), you can run this Python script to get the flag:

```python
# 1. Your given values (replace with the actual numbers)
p = 203427... # The long prime
A = 126884... # The server public key
b = ...        # The client secret exponent from file.txt
enc_hex = "..." # The hex string from file.txt (e.g., '4a5b...')

# 2. Reconstruct the shared secret
shared = pow(A, b, p)

# 3. Derive the 1-byte XOR key
key = shared % 256

# 4. Convert hex string to actual bytes
enc_bytes = bytes.fromhex(enc_hex)

# 5. XOR each byte with the key to get the characters
flag = ""
for byte in enc_bytes:
    # XOR the byte and convert back to a character
    decoded_char = chr(byte ^ key)
    flag += decoded_char

print(f"The Flag is: {flag}")
```

---

# Bonus: Brute Force

```python
enc_hex = "79606a664a5d4f726d61567a3a6a7b3a7d56303e6d6b316f3a3e74"
enc_bytes = bytes.fromhex(enc_hex)

for k in range(256):
    decoded = "".join([chr(b ^ k) for b in enc_bytes])
    if "pico" in decoded:
        print(f"Key found: {k}")
        print(f"Flag: {decoded}")
        break
```