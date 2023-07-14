from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_ship_ship_scan_response_201 import CreateShipShipScanResponse201
from ...types import Response


def _get_kwargs(
    ship_symbol: str,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/my/ships/{shipSymbol}/scan/ships".format(client.base_url, shipSymbol=ship_symbol)

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[CreateShipShipScanResponse201]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = CreateShipShipScanResponse201.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[CreateShipShipScanResponse201]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    ship_symbol: str,
    *,
    client: AuthenticatedClient,
) -> Response[CreateShipShipScanResponse201]:
    """Scan Ships

     Scan for nearby ships, retrieving information for all ships in range.

    Requires a ship to have the `Sensor Array` mount installed to use.

    The ship will enter a cooldown after using this function, during which it cannot execute certain
    actions.

    Args:
        ship_symbol (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateShipShipScanResponse201]
    """

    kwargs = _get_kwargs(
        ship_symbol=ship_symbol,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    ship_symbol: str,
    *,
    client: AuthenticatedClient,
) -> Optional[CreateShipShipScanResponse201]:
    """Scan Ships

     Scan for nearby ships, retrieving information for all ships in range.

    Requires a ship to have the `Sensor Array` mount installed to use.

    The ship will enter a cooldown after using this function, during which it cannot execute certain
    actions.

    Args:
        ship_symbol (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateShipShipScanResponse201
    """

    return sync_detailed(
        ship_symbol=ship_symbol,
        client=client,
    ).parsed


async def asyncio_detailed(
    ship_symbol: str,
    *,
    client: AuthenticatedClient,
) -> Response[CreateShipShipScanResponse201]:
    """Scan Ships

     Scan for nearby ships, retrieving information for all ships in range.

    Requires a ship to have the `Sensor Array` mount installed to use.

    The ship will enter a cooldown after using this function, during which it cannot execute certain
    actions.

    Args:
        ship_symbol (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateShipShipScanResponse201]
    """

    kwargs = _get_kwargs(
        ship_symbol=ship_symbol,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    ship_symbol: str,
    *,
    client: AuthenticatedClient,
) -> Optional[CreateShipShipScanResponse201]:
    """Scan Ships

     Scan for nearby ships, retrieving information for all ships in range.

    Requires a ship to have the `Sensor Array` mount installed to use.

    The ship will enter a cooldown after using this function, during which it cannot execute certain
    actions.

    Args:
        ship_symbol (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateShipShipScanResponse201
    """

    return (
        await asyncio_detailed(
            ship_symbol=ship_symbol,
            client=client,
        )
    ).parsed
