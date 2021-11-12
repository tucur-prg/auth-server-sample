import base64
import json
import hashlib
import hmac

class MyJWT:
    @classmethod
    def _b64decode(cls, value):
        rem = len(value) % 4
        if rem > 0:
            value += '=' * (4-rem)

        return base64.urlsafe_b64decode(value)
        
    @classmethod
    def _b64encode(cls, value):
        return base64.urlsafe_b64encode(value).decode("UTF-8").rstrip("=")

    @classmethod
    def _create_signature(cls, key, target, algorithm="HS256"):
        return hmac.new(
            key.encode("UTF-8"),
            target.encode("UTF-8"),
            hashlib.sha256
        ).digest()

    @classmethod
    def decode(cls, token, key):
        b64_header, b64_payload, b64_signature = token.split('.')

        raw_header = cls._b64decode(b64_header)
        raw_payload = cls._b64decode(b64_payload)
        raw_signature = cls._b64decode(b64_signature)

        payload = json.loads(raw_payload)

        signature = cls._create_signature(key, b64_header + '.' + b64_payload)
        if not hmac.compare_digest(signature, raw_signature):
            raise RuntimeError("invalid signature")

        return payload
        
    @classmethod
    def encode(cls, payload, key, algorithm="HS256"):
        header = {
            "typ": "JWT",
            "alg": algorithm,
        }

        raw_header = json.dumps(header, separators=(",", ":")).encode("UTF-8")
        raw_payload = json.dumps(payload, separators=(",", ":")).encode("UTF-8")

        b64_header = cls._b64encode(raw_header)
        b64_payload = cls._b64encode(raw_payload)

        signature = cls._create_signature(key, b64_header + '.' + b64_payload)
        b64_signature = cls._b64encode(signature)

        return b64_header + '.' + b64_payload + '.' + b64_signature
