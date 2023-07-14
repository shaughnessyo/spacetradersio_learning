from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.jump_ship_json_body import JumpShipJsonBody
from ...models.jump_ship_response_200 import JumpShipResponse200
from ...types import Response


def _get_kwargs(
    ship_symbol: str,
    *,
    client: AuthenticatedClient,
    json_body: JumpShipJsonBody,
) -> Dict[str, Any]:
    url = "{}/my/ships/{shipSymbol}/jump".format(client.base_url, shipSymbol=ship_symbol)

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[JumpShipResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = JumpShipResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[JumpShipResponse200]:
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
    json_body: JumpShipJsonBody,
) -> Response[JumpShipResponse200]:
    """Jump Ship

     Jump your ship instantly to a target system. The ship must be in orbit to use this function. When
    used while in orbit of a Jump Gate waypoint, any ship can use this command, jumping to the target
    system's Jump Gate waypoint.

    When used elsewhere, jumping requires the ship to have a `Jump Drive` module installed and consumes
    a unit of antimatter from the ship's cargo. The command will fail if there is no antimatter to
    consume. When jumping via the `Jump Drive` module, the ship ends up at its largest source of energy
    in the system, such as a gas planet or a jump gate.

    Args:
        ship_symbol (str):
        json_body (JumpShipJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JumpShipResponse200]
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
    json_body: JumpShipJsonBody,
) -> Optional[JumpShipResponse200]:
    """Jump Ship

     Jump your ship instantly to a target system. The ship must be in orbit to use this function. When
    used while in orbit of a Jump Gate waypoint, any ship can use this command, jumping to the target
    system's Jump Gate waypoint.

    When used elsewhere, jumping requires the ship to have a `Jump Drive` module installed and consumes
    a unit of antimatter from the ship's cargo. The command will fail if there is no antimatter to
    consume. When jumping via the `Jump Drive` module, the ship ends up at its largest source of energy
    in the system, such as a gas planet or a jump gate.

    Args:
        ship_symbol (str):
        json_body (JumpShipJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        JumpShipResponse200
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
    json_body: JumpShipJsonBody,
) -> Response[JumpShipResponse200]:
    """Jump Ship

     Jump your ship instantly to a target system. The ship must be in orbit to use this function. When
    used while in orbit of a Jump Gate waypoint, any ship can use this command, jumping to the target
    system's Jump Gate waypoint.

    When used elsewhere, jumping requires the ship to have a `Jump Drive` module installed and consumes
    a unit of antimatter from the ship's cargo. The command will fail if there is no antimatter to
    consume. When jumping via the `Jump Drive` module, the ship ends up at its largest source of energy
    in the system, such as a gas planet or a jump gate.

    Args:
        ship_symbol (str):
        json_body (JumpShipJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JumpShipResponse200]
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
    json_body: JumpShipJsonBody,
) -> Optional[JumpShipResponse200]:
    """Jump Ship

     Jump your ship instantly to a target system. The ship must be in orbit to use this function. When
    used while in orbit of a Jump Gate waypoint, any ship can use this command, jumping to the target
    system's Jump Gate waypoint.

    When used elsewhere, jumping requires the ship to have a `Jump Drive` module installed and consumes
    a unit of antimatter from the ship's cargo. The command will fail if there is no antimatter to
    consume. When jumping via the `Jump Drive` module, the ship ends up at its largest source of energy
    in the system, such as a gas planet or a jump gate.

    Args:
        ship_symbol (str):
        json_body (JumpShipJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        JumpShipResponse200
    """

    return (
        await asyncio_detailed(
            ship_symbol=ship_symbol,
            client=client,
            json_body=json_body,
        )
    ).parsed
