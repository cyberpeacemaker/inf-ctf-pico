
python3 -c "print(hex(0b101101110110010)[2:])"
echo -n 'zyzwg' | python3 -c "import sys; print(''.join('\\x{:02x}'.format(b) for b in sys.stdin.buffer.read()[::-1]))"


# bin operation (AND, OR, SHIFT)
```bash
python3 -c "print(bin(0b01111001 & 0b11000010)[2:].zfill(8))"
```
* **`0b...`**: Defines the number as binary.
* **`&`**: Performs the bitwise AND.
* **`bin(...)[2:]`**: Converts the result back to binary and strips the `0b` prefix.
* **`.zfill(8)`**: Ensures the output is 8 bits long (padding with zeros if necessary).

python3 -c "print(bin(0b00100011 << 1)[2:].zfill(8))"