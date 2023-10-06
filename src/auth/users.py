import uuid
from typing import Annotated

import httpx
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

import models
from core.config import settings
from core.utils import read_token as jwt_read_token

oauth_scheme = OAuth2PasswordBearer(tokenUrl='token')


class TokenReadingError(Exception):
    ...


class NotAuthorizedError(Exception):
    ...


async def read_token(token: str) -> models.User:
    try:
        contents = await jwt_read_token(
            token, settings.access_token_secret, audience=settings.access_token_audience
        )
    except jwt.exceptions.PyJWTError as e:
        raise TokenReadingError(str(e))

    user_id = contents.get('sub')
    if not user_id:
        raise TokenReadingError('Ivalid token: no user id found')
    rights = contents.get('rights')

    return models.User(id=user_id, rights=rights)


async def get_current_user(token: Annotated[str, Depends(oauth_scheme)]) -> models.User:
    try:
        user = await read_token(token)
    except TokenReadingError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user


async def get_current_user_with_permission(
    token: Annotated[str, Depends(oauth_scheme)], permission: str
) -> models.User:
    user = await get_current_user(token)

    if user.rights is None or permission not in user.rights:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return user


async def get_current_superuser(
    token: Annotated[str, Depends(oauth_scheme)]
) -> models.User:
    return await get_current_user_with_permission(token, settings.permissions_superuser)
