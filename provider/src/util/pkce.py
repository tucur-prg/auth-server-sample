import base64
import hashlib

S256 = "S256"
PLAIN = "plain"

def s256(value):
    h = hashlib.sha256(value).digest()
    b = base64.urlsafe_b64encode(h).rstrip(b'=')
    return b.decode()
