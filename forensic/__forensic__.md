#
Wireshark / tshark（封包分析）
Autopsy / FTK Imager（磁碟分析）
Volatility（記憶體分析）
#
binwalk（檔案分析與提取）
exiftool（檔案 metadata）
hexeditor
steghide、zsteg、stegsolve（隱寫術工具）

foremost / scalpel（檔案還原）
pdf-parser,A specialized tool to look at those specific Zlib objects Binwalk found.
- ELA, FotoForensics
---
# Wireshark / tshark
- `-T fields`: specific pieces of data."
- `-e`: data
The reason you were using xxd -r -p is that tshark -e tcp.payload outputs ASCII Hex (e.g., it prints the characters "f", "f", "d", "8"). To a computer, that is 4 bytes of text. The actual binary data is only 2 bytes. Without a tool to "un-hex" it, you just have a text file full of numbers.
Method,Output Type,Best Use Case
tshark -e tcp.payload | xxd,Binary,Quick extraction of specific packets.
tcpflow,Files,When you want to extract images/files sent over TCP.
"tshark -z ""follow...""",Binary,"Reconstructing a full ""conversation"" between two IPs."

- tshark -r myNetworkTraffic.pcap -T fields -e frame.time_relative -e tcp.payload

# General
- file, exiftool (`-s3`:short format lvl3), strings, binwalk
### 1. Embedded Structured Data (File-in-File)
This is when a completely separate, valid file is hidden inside another. 
* **The Technique:** Appending a `.zip` or `.png` to the end of a `.jpg`.
* **Why it works:** Many file formats have a "Length" field or an "End of File" marker. A computer stops reading once it hits that limit, ignoring the "bonus" file attached to the tail.
* **Best Tools:** `binwalk`, `foremost`, `scalpel`.

### 2. Embedded Raw Data (The "Trailing Bytes")
This is what you just found in the `garden.jpg` challenge.
* **The Technique:** Just pasting a string of text or raw bytes directly after the file's footer (like the `FF D9` in JPEGs).
* **Why it works:** Similar to the method above, the software only renders what it recognizes. It ignores the "extra" text because it isn't part of the image's mathematical data.
* **Best Tools:** `strings`, `xxd`, `hexdump`.

### 3. Steganography (Data *Within* Data)
This is the "pro" level where data isn't just *added* to the file, it is **woven into** the existing pixels or audio waves.
* **The Technique:** **LSB (Least Significant Bit)** encoding. You change the very last bit of the color value for thousands of pixels. For example, changing a pixel's color from `255, 255, 255` to `255, 255, 254` is invisible to the human eye, but those "1s" and "0s" can spell out a message.
* **Why it works:** The file size stays exactly the same, and there are no "extra" bytes at the end for `strings` to find. The data is part of the image itself.
* **Best Tools:** `steghide`, `stegsolve`, `zsteg`.

# Magic
- `kJggg==` PNG image file ends `IEND`file

Offset,Original Hex,Restored Hex,Meaning
00000000,5c78 (\x),ffd8,SOI (Start of Image)
00000002,ffe0,ffe0,APP0 (JFIF Marker)
00000006,4a46 4946,4a46 4946,JFIF identifier

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
`binwalk` is great at finding headers, but it often struggles to find the "End of File" marker

Plaintext: Has very few accidental signatures.
Encoded/Compressed Data: Because the characters are so "random" and packed together, the probability of a random sequence of bytes accidentally matching a "StuffIt Deluxe" or "ZBOOT" header is very high.
The "StuffIt Deluxe" Spam: Binwalk is seeing random Base64-looking strings and misidentifying them as "StuffIt" archive segments. This happens often with encrypted data or raw text that looks slightly like a file header.

Nonsense Headers: "IMG0 (VxWorks)" and "ZBOOT" are very common false positives when Binwalk encounters high-entropy data.

### "Manual" Approach (Precision Extraction)
- `dd if=flag2of2-final.pdf of=hidden_part.pdf bs=1 skip=914`
- `dd if=flag2of2-final.pdf of=hidden_image.png bs=1 count=914`
# steghide, stegseek
steghide info picture.jpg
-sf (stego file): The file that contains the hidden data.

# zsteg
Exactly! You hit the nail on the head. `zsteg` is essentially a **specialized brute-force engine** for bit manipulation.
For every combination it tries, it asks:
1.  **Is it text?** Does this look like ASCII/UTF-8?
2.  **Is it a known file?** Does it start with `PK..` (ZIP) or `\x89PNG`?
3.  **Is it "Entropy" high?** Does the data look like it has a pattern, or is it just random static?