from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.purchase_ship_json_body import PurchaseShipJsonBody
from ...models.purchase_ship_response_201 import PurchaseShipResponse201
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: PurchaseShipJsonBody,
) -> Dict[str, Any]:
    url = "{}/my/ships".format(client.base_url)

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[PurchaseShipResponse201]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = PurchaseShipResponse201.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[PurchaseShipResponse201]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: PurchaseShipJsonBody,
) -> Response[PurchaseShipResponse201]:
    """Purchase Ship

     Purchase a ship from a Shipyard. In order to use this function, a ship under your agent's ownership
    must be in a waypoint that has the `Shipyard` trait, and the Shipyard must sell the type of the
    desired ship.

    Shipyards typically offer ship types, which are predefined templates of ships that have dedicated
    roles. A template comes with a preset of an engine, a reactor, and a frame. It may also include a
    few modules and mounts.

    Args:
        json_body (PurchaseShipJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PurchaseShipResponse201]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: PurchaseShipJsonBody,
) -> Optional[PurchaseShipResponse201]:
    """Purchase Ship

     Purchase a ship from a Shipyard. In order to use this function, a ship under your agent's ownership
    must be in a waypoint that has the `Shipyard` trait, and the Shipyard must sell the type of the
    desired ship.

    Shipyards typically offer ship types, which are predefined templates of ships that have dedicated
    roles. A template comes with a preset of an engine, a reactor, and a frame. It may also include a
    few modules and mounts.

    Args:
        json_body (PurchaseShipJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PurchaseShipResponse201
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: PurchaseShipJsonBody,
) -> Response[PurchaseShipResponse201]:
    """Purchase Ship

     Purchase a ship from a Shipyard. In order to use this function, a ship under your agent's ownership
    must be in a waypoint that has the `Shipyard` trait, and the Shipyard must sell the type of the
    desired ship.

    Shipyards typically offer ship types, which are predefined templates of ships that have dedicated
    roles. A template comes with a preset of an engine, a reactor, and a frame. It may also include a
    few modules and mounts.

    Args:
        json_body (PurchaseShipJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PurchaseShipResponse201]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: PurchaseShipJsonBody,
) -> Optional[PurchaseShipResponse201]:
    """Purchase Ship

     Purchase a ship from a Shipyard. In order to use this function, a ship under your agent's ownership
    must be in a waypoint that has the `Shipyard` trait, and the Shipyard must sell the type of the
    desired ship.

    Shipyards typically offer ship types, which are predefined templates of ships that have dedicated
    roles. A template comes with a preset of an engine, a reactor, and a frame. It may also include a
    few modules and mounts.

    Args:
        json_body (PurchaseShipJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PurchaseShipResponse201
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
