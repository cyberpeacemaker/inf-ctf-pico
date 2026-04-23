#
Wireshark / tshark（封包分析）
Autopsy / FTK Imager（磁碟分析）
Volatility（記憶體分析）
#
binwalk（檔案分析與提取）
exiftool（檔案 metadata）
steghide、zsteg、stegsolve（隱寫術工具）

foremost / scalpel（檔案還原）
pdf-parser,A specialized tool to look at those specific Zlib objects Binwalk found.
- ELA, FotoForensics
foremost
hexeditor
---
- file, exiftool, strings, binwalk

# Magic
- `kJggg==` PNG image file ends `IEND`file

# hex edit
- hex editor, xxd + text editor, printf/echo + tail
- `echo "OFFSET: BYTES" | xxd -r - FILE`
### How to calculate the Offset accurately
1.  **Find the hex:** `printf '%x\n' 123` $\rightarrow$ returns `7b`.
2.  **Use it:** `echo "000007b: ff" | xxd -r - file.bin`
### Seek Alternative
**Example: Change bytes starting at decimal 50**
`echo "ffff" | xxd -r -p -s 50 file.bin`
*   **`-p`**: Tells `xxd` to expect a **plain** continuous hex string (no offsets/colons needed).
*   **`-s 50`**: Seeks to the 50th byte of the file before writing.
*   **`-`**: Tells it to take input from the pipe.

# binwalk
Binwalk works by looking for "Magic Bytes" (specific signatures like 89 50 4e 47 for PNG).

Plaintext: Has very few accidental signatures.

Encoded/Compressed Data: Because the characters are so "random" and packed together, the probability of a random sequence of bytes accidentally matching a "StuffIt Deluxe" or "ZBOOT" header is very high.

The "StuffIt Deluxe" Spam: Binwalk is seeing random Base64-looking strings and misidentifying them as "StuffIt" archive segments. This happens often with encrypted data or raw text that looks slightly like a file header.

Nonsense Headers: "IMG0 (VxWorks)" and "ZBOOT" are very common false positives when Binwalk encounters high-entropy data.

# steghide
steghide info picture.jpg
-sf (stego file): The file that contains the hidden data.