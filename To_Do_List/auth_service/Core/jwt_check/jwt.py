import jwt
from fastapi import HTTPException, status
from ..config.config import settings


@router.post("/check-refresh-token", status_code=status.HTTP_200_OK)
async def check_refresh_token(
    token_refresh: str | None = Cookie(alias=COOKIE_JWT_REFRESH, default=None),
):
    if token_refresh is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is missed",
        )
    try:
        payload = jwt.decode(
            jwt=token_refresh,
            key=settings.auth_jwt.publik_key.read_text(),
            algorithms=settings.auth_jwt.algorithm,
        )
        return payload
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token refresh expired",
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid refresh token"
        )


async def check_access_token(
    jwt_access: str | None, jwt_refresh: str | None
) -> dict | None:
    if jwt_access is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is missed",
        )
    try:
        payload = jwt.decode(
            jwt=jwt_access,
            key=settings.auth_jwt.publik_key.read_text(),
            algorithms=settings.auth_jwt.algorithm,
        )
        return payload
    except jwt.ExpiredSignatureError as e:
        return
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid access token"
        )
