from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.refuel_ship_json_body import RefuelShipJsonBody
from ...models.refuel_ship_response_200 import RefuelShipResponse200
from ...types import Response


def _get_kwargs(
    ship_symbol: str,
    *,
    client: AuthenticatedClient,
    json_body: RefuelShipJsonBody,
) -> Dict[str, Any]:
    url = "{}/my/ships/{shipSymbol}/refuel".format(client.base_url, shipSymbol=ship_symbol)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[RefuelShipResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = RefuelShipResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[RefuelShipResponse200]:
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
    json_body: RefuelShipJsonBody,
) -> Response[RefuelShipResponse200]:
    """Refuel Ship

     Refuel your ship by buying fuel from the local market.

    Requires the ship to be docked in a waypoint that has the `Marketplace` trait, and the market must
    be selling fuel in order to refuel.

    Each fuel bought from the market replenishes 100 units in your ship's fuel.

    Ships will always be refuel to their frame's maximum fuel capacity when using this action.

    Args:
        ship_symbol (str):
        json_body (RefuelShipJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RefuelShipResponse200]
    """

    kwargs = _get_kwargs(
        ship_symbol=ship_symbol,
        client=client,
        json_body=json_body,
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
    json_body: RefuelShipJsonBody,
) -> Optional[RefuelShipResponse200]:
    """Refuel Ship

     Refuel your ship by buying fuel from the local market.

    Requires the ship to be docked in a waypoint that has the `Marketplace` trait, and the market must
    be selling fuel in order to refuel.

    Each fuel bought from the market replenishes 100 units in your ship's fuel.

    Ships will always be refuel to their frame's maximum fuel capacity when using this action.

    Args:
        ship_symbol (str):
        json_body (RefuelShipJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RefuelShipResponse200
    """

    return sync_detailed(
        ship_symbol=ship_symbol,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    ship_symbol: str,
    *,
    client: AuthenticatedClient,
    json_body: RefuelShipJsonBody,
) -> Response[RefuelShipResponse200]:
    """Refuel Ship

     Refuel your ship by buying fuel from the local market.

    Requires the ship to be docked in a waypoint that has the `Marketplace` trait, and the market must
    be selling fuel in order to refuel.

    Each fuel bought from the market replenishes 100 units in your ship's fuel.

    Ships will always be refuel to their frame's maximum fuel capacity when using this action.

    Args:
        ship_symbol (str):
        json_body (RefuelShipJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RefuelShipResponse200]
    """

    kwargs = _get_kwargs(
        ship_symbol=ship_symbol,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    ship_symbol: str,
    *,
    client: AuthenticatedClient,
    json_body: RefuelShipJsonBody,
) -> Optional[RefuelShipResponse200]:
    """Refuel Ship

     Refuel your ship by buying fuel from the local market.

    Requires the ship to be docked in a waypoint that has the `Marketplace` trait, and the market must
    be selling fuel in order to refuel.

    Each fuel bought from the market replenishes 100 units in your ship's fuel.

    Ships will always be refuel to their frame's maximum fuel capacity when using this action.

    Args:
        ship_symbol (str):
        json_body (RefuelShipJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RefuelShipResponse200
    """

    return (
        await asyncio_detailed(
            ship_symbol=ship_symbol,
            client=client,
            json_body=json_body,
        )
    ).parsed
