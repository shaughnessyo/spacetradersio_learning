from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.accept_contract_response_200 import AcceptContractResponse200
from ...types import Response


def _get_kwargs(
    contract_id: str,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/my/contracts/{contractId}/accept".format(client.base_url, contractId=contract_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[AcceptContractResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = AcceptContractResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[AcceptContractResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    contract_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[AcceptContractResponse200]:
    """Accept Contract

     Accept a contract by ID.

    You can only accept contracts that were offered to you, were not accepted yet, and whose deadlines
    has not passed yet.

    Args:
        contract_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AcceptContractResponse200]
    """

    kwargs = _get_kwargs(
        contract_id=contract_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    contract_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[AcceptContractResponse200]:
    """Accept Contract

     Accept a contract by ID.

    You can only accept contracts that were offered to you, were not accepted yet, and whose deadlines
    has not passed yet.

    Args:
        contract_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AcceptContractResponse200
    """

    return sync_detailed(
        contract_id=contract_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    contract_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[AcceptContractResponse200]:
    """Accept Contract

     Accept a contract by ID.

    You can only accept contracts that were offered to you, were not accepted yet, and whose deadlines
    has not passed yet.

    Args:
        contract_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AcceptContractResponse200]
    """

    kwargs = _get_kwargs(
        contract_id=contract_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    contract_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[AcceptContractResponse200]:
    """Accept Contract

     Accept a contract by ID.

    You can only accept contracts that were offered to you, were not accepted yet, and whose deadlines
    has not passed yet.

    Args:
        contract_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AcceptContractResponse200
    """

    return (
        await asyncio_detailed(
            contract_id=contract_id,
            client=client,
        )
    ).parsed
