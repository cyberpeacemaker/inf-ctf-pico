# HTTP/S Protocal

- curl (Client URL)
- wget (WWW Get)
- nc (Netcat) (TCP/IP Swiss army knife) 

## Advanced

- gobuster / ffuf (guess urls based on wordlist)
- Burp Suite (Swiss Armpy Knife)
- sqlmap (Break into the Database)

# Session 
- application > storage > cookies
- netwrok > header > set-cookie

# CMD Session Cookie
document.cookie = "session_id=PASTE_COOKIE_HERE"; location.reload();

curl -H "Cookie: session=YbabaS6Rrk_9byeKFvH9oUyvDp0Iv0fIJg_JHqY9E5k" http://dolphin-cove.picoctf.net:58602/sessions
curl -s -b "session=12345" http://example.com/admin | grep "picoCTF"
-c (Cookie-jar): If the website gives you a new cookie after you log in, -c filename will save that new cookie to a file so you can use it in your next command.