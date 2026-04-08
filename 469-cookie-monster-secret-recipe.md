# URL
- `curl -v url`

If you want to automate sending data to that login.php form, curl is much easier than nc because it handles the HTTP headers for you: `curl -X POST -d "username=admin&password=password123" http://saturn.picoctf.net:1234/login.php`

Use nc when the challenge is a "raw" service (port 50000+, usually binary/pwn). Pipe your exploit strings from a file.

# cut, awk, grep
- cat payload | nc verbal-sleep.picoctf.net 60596 | grep "Set-Cookie" | cut -d'=' -f2 | cut -d';' -f1
- cat payload | nc verbal-sleep.picoctf.net 60596 | grep "Set-Cookie" | awk -F'[=;]' '{print $2}'
- cat payload | nc verbal-sleep.picoctf.net 60596 | grep -oP 'secret_recipe=\K[^;]+'

### URL encoding
```python
# Decode
echo "secret%3Drecipe" | python3 -c "import sys, urllib.parse; print(urllib.parse.unquote(sys.stdin.read().strip()))"

# Encode
echo "hello world" | python3 -c "import sys, urllib.parse; print(urllib.parse.quote(sys.stdin.read().strip()))"
```
```bash
# This works for decoding!
urldecode() {
    local data="${1//+/ }"
    printf '%b\n' "${data//%/\\x}"
}

urldecode "secret%3Drecipe"
```

### payload
```SHELL
POST /login.php HTTP/1.1
Host: verbal-sleep.picoctf.net:60596
Content-Type: application/x-www-form-urlencoded
Content-Length: 31
Connection: close

username=admin&password=password
```
cat payload - | nc verbal-sleep.picoctf.net 60596

### HTTP CRLF
- VIM  [:set ff=dos, insert Ctrl+V Ctrl+M > ^M]
- sed -i 's/$/\r/' payload