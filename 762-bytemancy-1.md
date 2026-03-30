#
python -c "print('e' * 1751)" | nc foggy-cliff.picoctf.net 65214
# chr (ASCII Decimals)
python -c "print(chr(101) * 1751)" | nc foggy-cliff.picoctf.net 65214
# pwntool
```python
from pwn import *

r = remote('foggy-cliff.picoctf.net', 65214)
r.sendlineafter(b'==> ', chr(101).encode() * 1751)
# If there was a second prompt:
# r.sendlineafter(b'Next prompt: ', b'second_answer')
r.interactive() # Drops you into a shell to see the output

```
# multi line
# Example if there were 3 prompts: 'e' * 1751, then 'a', then 'b'
python3 -c "print('e' * 1751 + '\n' + 'a' + '\n' + 'b')" | nc foggy-cliff.picoctf.net 65214