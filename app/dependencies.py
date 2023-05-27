import re
import time
from typing import Optional

import jwt
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app import JWT_ALGORITHM, JWT_AUDIENCE, JWT_ISSUING_ENTITY, JWT_PUBLIC_KEY


def get_token_expiration_time_string(token_expiration_epoch_seconds: int) -> str:
    current_epoch_seconds: int = int(time.time())
    token_expiration_time_ago: int = (
        current_epoch_seconds - token_expiration_epoch_seconds
    )

    token_age_days: int = token_expiration_time_ago // 86400
    token_age_hours: int = token_expiration_time_ago // 3600 % 24
    token_age_minutes: int = token_expiration_time_ago // 60 % 60
    token_age_seconds = token_expiration_time_ago % 60

    token_age_bits: list[str] = []
    if token_age_days:
        token_age_bits.append(f"{token_age_days} days")
    if token_age_hours:
        token_age_bits.append(f"{token_age_hours} hours")
    if token_age_minutes:
        token_age_bits.append(f"{token_age_minutes} minutes")
    token_age_bits.append(f"{token_age_seconds} seconds")

    return ", ".join(token_age_bits)


class Object(object):
    def __init__(self, *args):
        self._args = args

    def __repr__(self):
        return " ".join(map(str, self._args))


class Authenticate(HTTPBearer):
    def __init__(
        self,
        auto_error: bool = True,
    ):
        super(Authenticate, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> str:
        credentials: HTTPAuthorizationCredentials = await super(
            Authenticate, self
        ).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                # 401 because we can't authenticate...cannot figure out who they are.
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication scheme",
                )

            request_identity = Object()

            expired_time_ago: str | None = None

            # JWT library handles expiration, issuer, and audience checks
            try:
                decoded_token: str = jwt.decode(
                    credentials.credentials,
                    JWT_PUBLIC_KEY,
                    algorithms=[JWT_ALGORITHM],
                    issuer=JWT_ISSUING_ENTITY,
                    options={"verify_exp": False, "verify_aud": False},
                )

                if "exp" not in decoded_token:
                    raise jwt.MissingRequiredClaimError("Missing expiration claim")

                if decoded_token["exp"] < time.time():
                    expiration_time_ago: str = get_token_expiration_time_string(
                        decoded_token["exp"]
                    )
                    raise jwt.ExpiredSignatureError(time.time() - decoded_token["exp"])

                if "aud" not in decoded_token:
                    raise jwt.MissingRequiredClaimError("Missing audience claim")

                if JWT_AUDIENCE not in decoded_token["aud"]:
                    raise jwt.InvalidAudienceError("Bad audience claim")
            except jwt.ExpiredSignatureError:
                raise HTTPException(
                    detail=f"JWT: Expired: The JWT expired {expiration_time_ago} ago",
                    status_code=status.HTTP_403_FORBIDDEN,
                )
            except jwt.InvalidAudienceError:
                raise HTTPException(
                    detail=f"JWT: Invalid audience: actual: {decoded_token['aud']}; expected: {JWT_AUDIENCE}",
                    status_code=status.HTTP_403_FORBIDDEN,
                )
            except jwt.InvalidIssuerError:
                raise HTTPException(
                    detail=f"JWT Invalid issuer: actual: {decoded_token['iss']}; expected: {JWT_ISSUING_ENTITY}",
                    status_code=status.HTTP_403_FORBIDDEN,
                )
            except jwt.MissingRequiredClaimError:
                raise HTTPException(
                    detail=f"JWT:  Missing required claim--your token does not have an expiration timestamp",
                    status_code=HTTP_403_FORBIDDEN,
                )
            except jwt.DecodeError:
                raise HTTPException(
                    detail=f"JWT DecodeError occured. Please check that your JWT is valid.",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                )
            else:
                request_identity.username = decoded_token["sub"]
                # Perhaps add other attributes to request_identity such as groups
        else:
            raise HTTPException(
                detail="Couldn't find credentials",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        request.state.identity = request_identity

        return HTTPAuthorizationCredentials(
            scheme=credentials.scheme, credentials=credentials.credentials
        )
