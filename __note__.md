- rm !(README.txt)
- sz <filename> / rz.

---

# text
- sed 's/==.*/==/'

- cat payload | nc verbal-sleep.picoctf.net 60596 | grep "Set-Cookie" | cut -d'=' -f2 | cut -d';' -f1
- cat payload | nc verbal-sleep.picoctf.net 60596 | grep "Set-Cookie" | awk -F'[=;]' '{print $2}'
- cat payload | nc verbal-sleep.picoctf.net 60596 | grep -oP 'secret_recipe=\K[^;]+'

- grep -oP 'text: "\K.*?=='
- awk '{print $2}'
- sort -n
- cat xd | tr -d '[:space:]'
- cat xxd_str | cut -c 4- | xxd -r -p ; echo ""

# file
1.  **`file`** (What is it actually?)
2.  **`exiftool`** (What does the metadata say?)
3.  **`strings -n 8`** (Are there long text strings?)
4.  **`binwalk -e`** (Is there another file inside?)
5.  **`stegsolve` / `zsteg`** (Is it hidden in the pixels?)

# url
- curl arg

### payload
```SHELL
POST /login.php HTTP/1.1
Host: verbal-sleep.picoctf.net:60596
Content-Type: application/x-www-form-urlencoded
Content-Length: 31
Connection: close

username=admin&password=password
```
**HTTP CRLF**
- VIM  [:set ff=dos, insert Ctrl+V Ctrl+M > ^M]
- sed -i 's/$/\r/' payload

# encode
xxd -b A

To read those "0/1" characters as actual bits, you need to convert them from a string of text into a raw binary value.

### 1. The "Quick & Dirty" Way (using `bc`)
The `bc` (Arbitrary Precision Calculator) tool is excellent for base conversions. You can tell it the input is binary (base 2) and the output should be hex or ASCII.

```bash
# Convert the string of 0/1s to Hex
echo "obase=16; ibase=2; $(cat bin_A)" | bc
```
**Output:** `41` (which is the hex for 'A')

### 3. Using Perl (The "Professional" Way)
If you are doing this in a CTF, Perl is often the most reliable way to pack strings of bits into actual raw bytes:

```bash
perl -lpe '$_ = pack("B*", $_)' bin_A
```
* **`pack("B*", ...)`**: This function takes a string of 1s and 0s and "packs" them into a binary structure.


-
# Fei Fei
https://path.feifei.tw/#path-5

2.1 🌐 Web Security（網頁安全）
這是最適合新手入門的領域，門檻較低且題目豐富。

核心知識點：

SQL Injection（SQL 注入）
XSS（跨站腳本攻擊）
CSRF（跨站請求偽造）
SSRF（伺服器端請求偽造）
檔案上傳漏洞
路徑穿越（Path Traversal）
反序列化漏洞
必學工具：

Burp Suite（攔截與修改請求）
curl / wget（命令列請求工具）
Browser DevTools（瀏覽器開發者工具）
sqlmap（自動化 SQL 注入工具）
dirsearch / gobuster（目錄掃描）
學習資源：

PortSwigger Web Security Academy（強烈推薦）
OWASP Top 10
Hack The Box - Web Challenges
2.2 🔓 Cryptography（密碼學）
學習各種加密演算法的原理與破解方式。

核心知識點：

古典密碼：Caesar、Vigenère、Substitution
對稱加密：AES、DES
非對稱加密：RSA、ECC
雜湊函數：MD5、SHA 系列
編碼：Base64、Hex、ASCII
必學工具：

CyberChef（萬用解碼工具）
Python 的 pycryptodome 套件
RsaCtfTool
hashcat / John the Ripper（密碼破解）
SageMath（數學運算）
學習資源：

CryptoHack（互動式學習平台，強推）
Crypto101（免費電子書）
2.3 🔧 Reverse Engineering（逆向工程）
分析程式的運作邏輯，找出隱藏的 flag。

核心知識點：

組合語言基礎（x86/x64）
可執行檔格式（ELF、PE）
靜態分析 vs 動態分析
反編譯與反組譯
常見混淆手法
必學工具：

Ghidra（免費，功能強大）
IDA Free / IDA Pro
Radare2 / Cutter
GDB + pwndbg / GEF（動態調試）
x64dbg（Windows 調試）
strings、objdump、readelf
學習資源：

Nightmare（逆向工程完整教程）
Reverse Engineering for Beginners（免費電子書）
crackmes.one（練習平台）
2.4 💥 Pwn / Binary Exploitation（二進位漏洞利用）
這是難度最高但也最有趣的領域，需要較多先備知識。

核心知識點：

記憶體布局（Stack、Heap、BSS、Data）
Buffer Overflow（緩衝區溢位）
Return Oriented Programming (ROP)
Format String Vulnerability
Heap Exploitation
保護機制：ASLR、NX、Canary、PIE、RELRO
必學工具：

pwntools（Python 漏洞利用框架）
GDB + pwndbg / GEF
ROPgadget / ropper
one_gadget
checksec
學習資源：

pwn.college（ASU 開設的免費課程，超推）
ROP Emporium（ROP 專項練習）
how2heap（Heap 利用教學）
建議學習順序：

Stack Overflow → Return to libc → ROP → Format String → Heap
2.5 🔍 Forensics（數位鑑識）
分析各種數位證據，從中找出隱藏資訊。

核心知識點：

檔案格式分析（圖片、文件、壓縮檔）
隱寫術（Steganography）
記憶體鑑識（Memory Forensics）
網路封包分析
磁碟映像分析
日誌分析
必學工具：

Wireshark / tshark（封包分析）
Autopsy / FTK Imager（磁碟分析）
Volatility（記憶體分析）
binwalk（檔案分析與提取）
exiftool（檔案 metadata）
steghide、zsteg、stegsolve（隱寫術工具）
foremost / scalpel（檔案還原）
學習資源：

DFIR Training
13Cubed YouTube