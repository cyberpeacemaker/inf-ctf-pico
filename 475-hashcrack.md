
# Identify Hash Algo
- length
- structure

Identifying a hash by sight is a bit like being a digital detective. Since hashes are just hexadecimal strings, they can look identical at first glance, but their **length** and **character set** are the smoking guns.

Here is the "beginner to pro" workflow for identifying them:

### 1. The "Cheat Sheet" (Length-Based)
Most common hashes have a fixed length. You can count the characters to narrow it down instantly.

| Length (Chars) | Common Hash Type | Hashcat Mode (`-m`) |
| :--- | :--- | :--- |
| **32** | MD5 | `0` |
| **40** | SHA-1 | `100` |
| **64** | SHA-256 | `1400` |
| **128** | SHA-512 | `1700` |
| **32** | NTLM (Windows) | `1000` |

> **Note:** Notice MD5 and NTLM are both 32 characters. To tell them apart, look at the context. If it's from a Windows `SAM` file, it’s NTLM. If it's from a web database, it's likely MD5.

---

### 2. Use Automated Identification Tools
Don't guess if you don't have to. There are tools built specifically to analyze the entropy and format of a string.

* **`hash-identifier`:** A classic command-line tool (pre-installed on Kali). Just run the command, paste your hash, and it gives you a list of "Possible" and "Least Possible" types.
* **`Name-That-Hash` (nth):** The modern replacement for hash-identifier. It's much faster and provides the specific **Hashcat mode numbers** in the output.
    * *Command:* `nth -s <your_hash_here>`
* **`haiti`:** Another excellent CLI tool that identifies hashes and even provides sample hashes for comparison.

---

### 3. Look for "Signatures" (The Prefixes)
Modern, more secure hashes (like those used for Linux passwords) often include a signature at the beginning to tell the system how to read them.



* **`$1$`** : MD5-based crypt
* **`$2a$`** or **`$2y$`** : **Bcrypt** (Very common in web apps)
* **`$5$`** : SHA-256 crypt
* **`$6$`** : SHA-512 crypt (Standard for modern Linux `/etc/shadow`)
* **`$argon2i$`** : Argon2 (The current high-security standard)

---

### 4. Use the Hashcat Example Page
If you have a hash that looks weird (e.g., it has a colon `:` or a salt attached), go to the **[Hashcat Example Hashes Wiki](https://hashcat.net/wiki/doku.php?id=example_hashes)**.

1.  Press `Ctrl + F` on that page.
2.  Paste a small piece of your hash (or search for the prefix).
3.  Match your format to the example to find the exact mode number.

### 5. Check the Context
In a CTF like **picoCTF**, the file name or the challenge description is often a hint:
* File is `config.php`? Likely **MD5** or **Bcrypt**.
* File is a packet capture (`.pcap`)? Likely **Kerberos** or **WPA2/PMKID**.
* File is from a database dump? Check if there is a "salt" column next to the "password" column.

---

### Summary Checklist
1.  **Count the characters.**
2.  **Check for prefixes** (like `$6$`).
3.  **Run `nth` or `hash-identifier`.**
4.  **Match against Hashcat examples.**

**Do you have a specific hash string right now that you're trying to identify? I can help you break it down.**

# Hashcat
Dictionary + Rule

### 2. Dictionary Attacks with "Rules" (Hybrid)
Pure dictionary attacks often fail because users add a single number or capital letter. Attackers counter this using **rules** to transform dictionary words.
* **Common Transformations:**
    * **Capitalization:** `password` → `Password`
    * **Appending Years:** `password` → `password2024`
    * **L33tspeak:** `password` → `p4ssw0rd`
* **Tooling:** Hashcat is famous for its `.rule` files that automate thousands of these variations per dictionary word.

##

Hashcat is the "Ferrari" of password cracking—it's incredibly fast, but it has a lot of buttons and can "crash" your system if you aren't careful. Since you are starting with picoCTF or similar forensics, here are the most important tips to move from a beginner to a power user.

---

### 1. Identify the Hash Type First
Hashcat doesn't "auto-detect" hash types like John the Ripper does. You must tell it exactly what it’s looking at using the `-m` (mode) flag.
* **Common Modes:**
    * **MD5:** `-m 0`
    * **SHA-1:** `-m 100`
    * **NTLM (Windows):** `-m 1000`
    * **SHA-256:** `-m 1400`
* **Pro Tip:** Use the [Hashcat Example Wiki](https://hashcat.net/wiki/doku.php?id=example_hashes) to match your hash's format to the correct mode number.

### 2. Master the "Attack Modes"
Don't just stick to one way of cracking. Hashcat has several "modes" (`-a` flag):
* **`-a 0` (Straight/Dictionary):** Simplest. Compares your hash against a wordlist (like `rockyou.txt`).
* **`-a 3` (Brute-force/Mask):** Use this when you know the password structure. 
    * Example: `?u?l?l?l?d?d` will try one Uppercase, three Lowercase, and two Digits (e.g., `Pass12`).
* **`-a 1` (Combinator):** Combines two wordlists. If `list1` has "Admin" and `list2` has "123", it tries "Admin123".

### 3. Use "Rules" to Supercharge Wordlists
Instead of downloading a 100GB wordlist, take a small 10MB list and apply **Rules** (`-r`). This tells Hashcat to mutate every word (capitalize it, reverse it, add "123" to the end, etc.).
* **The Best Starter Rule:** Use `best64.rule` (usually found in `/usr/share/hashcat/rules/`).
* **Command:** `hashcat -m 0 hash.txt rockyou.txt -r best64.rule`

### 4. Manage Your Hardware
Hashcat uses your GPU, which can get **very hot**.
* **Check Stats:** Press `s` while it’s running to see the temperature and speed (H/s).
* **Workload Tuning:** If your computer becomes laggy while cracking, add `-w 2` (Workload profile: Default) or `-w 1` (Low) to the command. `-w 3` is "High" and might freeze your screen.

---

### 5. Use the "Potfile"
Hashcat stores every password it has ever cracked in a file called `hashcat.potfile`. 
* If you try to crack the same hash twice, Hashcat will say "Cracked" immediately without running. 
* If you want to see the results of a previous crack, use the `--show` flag: 
    `hashcat -m 0 hash.txt --show`

---

### Useful Shortcuts (While Running)
| Key | Action |
| :--- | :--- |
| **s** | **Status:** Shows temp, speed, and estimated time remaining. |
| **p** | **Pause:** Useful if you need to use your PC for something else briefly. |
| **r** | **Resume:** Gets back to work. |
| **q** | **Quit:** Safely stops the process. |



**Would you like me to help you craft a specific "Mask Attack" command for a password you suspect follows a certain pattern?**

# Rainbow table

### 1. The "Big Three" Tools (Software)
These are the tools you would install (usually found pre-installed on Kali Linux) to use rainbow tables you’ve downloaded or generated yourself.

* **RainbowCrack (`rcrack`):** The absolute gold standard for this method. It’s a suite of tools (`rtgen` to generate, `rtsort` to organize, and `rcrack` to search). It’s highly optimized for multi-core CPUs and GPU acceleration (NVIDIA/AMD).
* **Ophcrack:** Specifically famous for cracking Windows passwords (LM and NTLM hashes). It’s incredibly user-friendly and often comes as a "Live CD"—you boot a locked computer from the disc, and it automatically finds and cracks the Windows login passwords in seconds using its built-in tables.
* **Cain and Abel:** An older but legendary "Swiss Army Knife" for Windows. While it does many things (sniffing, routing protocol analysis), it has a very solid rainbow table lookup engine for various hash types.

---

### 2. Common Lookup Websites (Instant Results)
If you only have one or two hashes and don't want to download 500GB of tables, these websites do the lookup for you. They have already computed trillions of hashes.

* **CrackStation:** Likely the most famous. It uses massive lookup tables (not strictly "rainbow tables" in the mathematical sense, but a similar pre-computed result) for MD5, SHA1, and many others. It is often the first stop for CTF players.
* **Hashes.com:** A community-driven "escrow" and lookup site. You can search their database for free to see if a hash has already been cracked by someone else.
* **OnlineHashCrack:** A service where you can upload a hash (or even a handshake file from a WiFi network) and they will run it against their massive hardware clusters and pre-computed tables.

---