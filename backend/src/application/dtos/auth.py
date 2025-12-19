from dataclasses import dataclass


@dataclass(frozen=True)
class AuthResultDTO:
    access_token: str