import typing
import uuid
from uuid import UUID

import backoff
import httpx
import orjson
from services.abc import UserServiceABC

from core.config import authorization_data, user_properties
from core.logger import logger
from models.users import NotificationChannel, User, UserChannels

LOGGER = logger()


class UserService(UserServiceABC):
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def get_users(self, user_ids: typing.Iterable[UUID]) -> typing.Iterable[User]:
        body = orjson.dumps({"ids": [str(uid) for uid in user_ids]})
        users = await self._get_request_with_body(user_properties.url_get_users, body)

        serialized_users = await self._serialize_users(users)

        return serialized_users

    @backoff.on_exception(backoff.expo, httpx.RequestError, max_tries=5)
    async def _get_request_with_body(
        self, url: str, body: typing.Mapping[str, typing.Any]
    ) -> typing.Iterable[typing.Mapping[str, typing.Any]]:
        """
        Does the get request associated with the given body.

        Args:
            url (str): The url of the request.
            body (dict[str, typing.Any]): A body of request.

        Returns:
            dict: A dictionary containing the response JSON if the request is successful.

        Raises:
            HTTPError: If the request fails with a non-200 status code.
        """
        # url = user_properties.url_get_users_channels
        access_token = await self._get_access_token()
        headers = {
            'Content-Type': "application/json",
            'X-Request-Id': str(uuid.uuid4()),
            'Authorization': f'Bearer {access_token}',
        }

        request = httpx.Request('GET', url, data=body, headers=headers)
        response = await self.client.send(request=request)
        if response.status_code != 200:
            response.raise_for_status()

        return response.json()

    async def _serialize_users(
        self, _users: typing.Iterable[typing.Mapping[str, typing.Any]]
    ) -> typing.Iterable[User]:
        """
        Serializes a list of users.

        Args:
            _users (list[dict]): A list of dictionaries representing users.

        Returns:
            list (User): The serialized user channels.

        Raises:
            Exception: If there is an error during serialization.
        """

        users = []

        try:
            users = [User(**user) for user in _users]
        except Exception as e:
            LOGGER.error(f"Invalid user: {_users}. {e}")

        return users

    async def _get_access_token(self) -> str | None:
        refresh_token = await self._get_refresh_token()

        url = user_properties.url_refresh_token
        headers = {
            'X-Request-Id': str(uuid.uuid4()),
            'Authorization': f'Bearer {refresh_token}',
        }
        request = httpx.Request('POST', url, headers=headers)
        response = await self.client.send(request=request)
        LOGGER.info(response.status_code)
        if response.status_code == 200:
            access_token = response.json()['access_token']
            await self._set_access_token(access_token)
            return access_token
        response.raise_for_status()

    async def _get_refresh_token(self) -> str | None:

        url = user_properties.url_login
        headers = {'X-Request-Id': str(uuid.uuid4())}
        data = {
            "username": user_properties.username,
            "password": user_properties.password,
        }
        response = await self.client.post(url=url, headers=headers, data=data)
        if response.status_code == 200:
            refresh_token = response.json()['refresh_token']
            await self._set_refresh_token(refresh_token)
            return refresh_token
        response.raise_for_status()

    async def _set_access_token(self, access_token):
        authorization_data['access_token'] = access_token

    async def _set_refresh_token(self, refresh_token):
        authorization_data['refresh_token'] = refresh_token


async def get_user_service() -> typing.AsyncGenerator[UserService, None]:
    yield UserService(httpx.AsyncClient())
