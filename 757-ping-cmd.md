# Shell Injection

### Common Command Separators
In Linux shells, you can chain commands together using these special characters:

* **`;` (Semicolon):** Executes the second command after the first one finishes.
* **`&` (Background):** Executes the first command in the background and immediately starts the second.
* **`&&` (AND):** Executes the second command only if the first one succeeds.
* **`||` (OR):** Executes the second command only if the first one fails.
* **`|` (Pipe):** Passes the output of the first command as input to the second.
* **`\n` (Newline):** Often works if the input is processed line-by-line.

---

### Potential Payloads
Since the system specifically looks for `8.8.8.8`, you need to include that string while "breaking out" of the intended command.

**1. The Semicolon Trick**
If the backend is doing something like `system("ping -c 1 " + input)`, you can try:
`8.8.8.8; ls`
*This runs the ping, then lists the files.*

**2. The Pipe Trick**
If they are using a regex that just checks if the string *starts* with 8.8.8.8:
`8.8.8.8 | ls`

**3. The Inline Subshell**
If they wrap your input in quotes, you might need to use backticks or `$()` to execute code:
`8.8.8.8 $(ls)`

---

### Bypassing "Tight Security"
If the "tight security" means they are filtering spaces or certain characters, you can try these alternatives:

| Restriction | Bypass Alternative | Example |
| :--- | :--- | :--- |
| **No Spaces** | Use `${IFS}` (Internal Field Separator) | `8.8.8.8;ls${IFS}-la` |
| **Only 8.8.8.8 allowed** | Comment out the rest | `ls; # 8.8.8.8` |
| **Input must end with 8.8.8.8** | Prepend command | `ls && ping -c 1 8.8.8.8` |



### Recommendation
Start by trying to see if you can get a simple directory listing. Once you confirm the injection works, you can look for that `flag.txt` you were working on earlier:

```bash
8.8.8.8; cat flag.txt
```

**Would you like me to explain how to use `base64` encoding to bypass filters if the server is blocking keywords like "cat" or "flag"?**