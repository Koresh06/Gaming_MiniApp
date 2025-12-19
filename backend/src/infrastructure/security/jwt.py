from datetime import datetime, timedelta, timezone
import jwt


class JWTService:
    def __init__(self, secret: str, algorithm: str, ttl_minutes: int):
        self.secret = secret
        self.algorithm = algorithm
        self.ttl = ttl_minutes

    def create_token(self, subject: str) -> str:
        payload = {
            "sub": subject,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=self.ttl),
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def decode_token(self, token: str) -> dict:
        return jwt.decode(token, self.secret, algorithms=[self.algorithm])
