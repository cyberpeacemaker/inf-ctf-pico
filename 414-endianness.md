
# opt 1
echo -n 'zyzwg' | xxd -p > str_hex
echo -n 'zyzwg' | xxd -p | python3 -c "import sys; print(bytes.fromhex(sys.stdin.read().strip())[::-1].hex())"

# opt 2
echo -n 'zyzwg' | python3 -c "print(sys.stdin.read()[::-1].encode().hex())"

# opt 3 
echo -n 'zyzwg' | python3 -c "import sys; print(sys.stdin.buffer.read()[::-1].hex())"

# Bonus
### Comparative Examples
If you want to hardcode the string into the command rather than piping it, you can use the `b''` prefix directly:

| Method | Command | Result |
| :--- | :--- | :--- |
| **Direct Bytes** | `python3 -c "print(b'zyzwg'[::-1].hex())"` | `67777a797a` |
| **Hex to Bytes** | `python3 -c "print(bytes.fromhex('7a797a7767')[::-1].hex())"` | `67777a797a` |

---

### Pro-Tip: Formatting for Payloads
If your "continuous steps" involve using this hex in an exploit (like a buffer overflow), you might need it in the `\x67\x77` format. You can do that easily by changing the print logic:

```bash
echo -n 'zyzwg' | python3 -c "import sys; print(''.join('\\x{:02x}'.format(b) for b in sys.stdin.buffer.read()[::-1]))"
```
**Output:** `\x67\x77\x7a\x79\x7a`
