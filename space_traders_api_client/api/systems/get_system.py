from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_system_response_200 import GetSystemResponse200
from ...types import Response


def _get_kwargs(
    system_symbol: str = "X1-OE",
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/systems/{systemSymbol}".format(client.base_url, systemSymbol=system_symbol)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[GetSystemResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetSystemResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[GetSystemResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    system_symbol: str = "X1-OE",
    *,
    client: AuthenticatedClient,
) -> Response[GetSystemResponse200]:
    """Get System

     Get the details of a system.

    Args:
        system_symbol (str):  Default: 'X1-OE'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetSystemResponse200]
    """

    kwargs = _get_kwargs(
        system_symbol=system_symbol,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    system_symbol: str = "X1-OE",
    *,
    client: AuthenticatedClient,
) -> Optional[GetSystemResponse200]:
    """Get System

     Get the details of a system.

    Args:
        system_symbol (str):  Default: 'X1-OE'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetSystemResponse200
    """

    return sync_detailed(
        system_symbol=system_symbol,
        client=client,
    ).parsed


async def asyncio_detailed(
    system_symbol: str = "X1-OE",
    *,
    client: AuthenticatedClient,
) -> Response[GetSystemResponse200]:
    """Get System

     Get the details of a system.

    Args:
        system_symbol (str):  Default: 'X1-OE'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetSystemResponse200]
    """

    kwargs = _get_kwargs(
        system_symbol=system_symbol,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    system_symbol: str = "X1-OE",
    *,
    client: AuthenticatedClient,
) -> Optional[GetSystemResponse200]:
    """Get System

     Get the details of a system.

    Args:
        system_symbol (str):  Default: 'X1-OE'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetSystemResponse200
    """

    return (
        await asyncio_detailed(
            system_symbol=system_symbol,
            client=client,
        )
    ).parsed
