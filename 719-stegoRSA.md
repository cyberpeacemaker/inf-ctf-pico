wget https://challenge-files.picoctf.net/c_plain_mesa/57932cef0608e6ef25a588a427a485649b572fe08ade8e7888f12fd7a43dca95/flag.enc
wget https://challenge-files.picoctf.net/c_plain_mesa/57932cef0608e6ef25a588a427a485649b572fe08ade8e7888f12fd7a43dca95/image.jpg
exiftool image.jpg | grep -i "comment" | awk -F ': ' '{print $2}' > hexkey.pkey
xxd -r -p hexkey.pkey key.pkey
openssl pkeyutl -decrypt -inkey key.pkey -in flag.enc -out flag.txt
cat flag.txt

# xxd, base64
- base64
- xxd (Hex Dump)

# grep, sed, awk, tr

| Tool | Primary Purpose | Best For... |
| :--- | :--- | :--- |
| **grep** | **Searching** | Finding a specific string, pattern, or flag format. |
| **sed** | **Editing** | Replacing text strings or deleting specific lines. |
| **awk** | **Processing** | Extracting columns or handling "Label : Value" data. |
| **tr** | **Translating** | Character-level swapping (like ROT13) or deleting sets. |

- grep (**Global Regular Expression Print**)
- sed (Stream Editor)
- awk (Alfred Aho, Peter Weinberger, Brian Kernighan)
- tr (translate)

# Decrption PKCS#1 v1.5 OSEP
`openssl pkeyutl -decrypt -inkey private.key -in flag.enc -out flag.txt`
If the command above gives an error like RSA_padding_check_PKCS1_type_2:block type is not 02, it means the encryption used a different padding scheme. You can specify the padding manually:
`openssl pkeyutl -decrypt -inkey private.key -in flag.enc -out flag.txt -pkeyopt rsa_padding_mode:oaep`

# Not Standard RSA encryption
Sometimes "RSA" challenges are actually just raw math. If the OpenSSL command fails, you might need to extract the numbers ($n$, $e$, $d$) from the key to perform the math manually in Python ($m = c^d \pmod n$).You can view the raw parameters of your key with:
`openssl rsa -in private.key -text -noout`