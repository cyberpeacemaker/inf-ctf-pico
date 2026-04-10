# objdump, excutable instruction, rodata
### Why was it in `strings` but not in `objdump`?

1.  **`static.ltdis.strings.txt`**: The `strings` utility scans the **entire binary** (including data sections like `.rodata`, where "Read-Only Data" constants are stored). Since the flag was a hardcoded string constant, `strings` found it easily.
2.  **`static.ltdis.x86_64.txt`**: Your `objdump` command specifically targeted the **`.text` section** (`-j .text`). The `.text` section contains **executable instructions** (code), not the data itself.

