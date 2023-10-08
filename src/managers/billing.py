import typing as t
import uuid
from uuid import UUID

import backoff
import httpx

import models
from core.config import settings


class BillingManager:
    def __init__(self):
        pass

    async def get_ivoice(self, id_: UUID) -> models.InvoiceRead:
        raise NotImplemented

    async def get_ivoice_by_account(self, id_: UUID) -> t.Iterable[models.Invoice]:
        raise NotImplemented

    async def create_invoice(self, invoice: models.InvoiceCreate) -> models.InvoiceRead:
        body = invoice.model_dump_json()
        invoice = await self._create_invoice(body, settings.url_create_invoice)
        return models.InvoiceRead.model_validate_json(invoice)

    async def create_refund(self, invoice_id) -> models.InvoiceRead:
        ...

    @backoff.on_exception(backoff.expo, httpx.RequestError, max_tries=5)
    async def _get_request_with_body(
        self, url: str, body: t.Mapping[str, t.Any]
    ) -> t.Iterable[t.Mapping[str, t.Any]]:
        """
        Does the get request associated with the given body.

        Args:
            url (str): The url of the request.
            body (dict[str, t.Any]): A body of request.

        Returns:
            dict: A dictionary containing the response JSON if the request is successful.

        Raises:
            HTTPError: If the request fails with a non-200 status code.
        """
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
