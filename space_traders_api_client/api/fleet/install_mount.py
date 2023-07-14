from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.install_mount_install_mount_201_response import InstallMountInstallMount201Response
from ...models.install_mount_install_mount_request import InstallMountInstallMountRequest
from ...types import Response


def _get_kwargs(
    ship_symbol: str,
    *,
    client: AuthenticatedClient,
    json_body: InstallMountInstallMountRequest,
) -> Dict[str, Any]:
    url = "{}/my/ships/{shipSymbol}/mounts/install".format(client.base_url, shipSymbol=ship_symbol)

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[InstallMountInstallMount201Response]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = InstallMountInstallMount201Response.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[InstallMountInstallMount201Response]:
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
    json_body: InstallMountInstallMountRequest,
) -> Response[InstallMountInstallMount201Response]:
    """Install Mount

     Install a mount on a ship.

    In order to install a mount, the ship must be docked and located in a waypoint that has a `Shipyard`
    trait. The ship also must have the mount to install in its cargo hold.

    An installation fee will be deduced by the Shipyard for installing the mount on the ship.

    Args:
        ship_symbol (str):
        json_body (InstallMountInstallMountRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[InstallMountInstallMount201Response]
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
    json_body: InstallMountInstallMountRequest,
) -> Optional[InstallMountInstallMount201Response]:
    """Install Mount

     Install a mount on a ship.

    In order to install a mount, the ship must be docked and located in a waypoint that has a `Shipyard`
    trait. The ship also must have the mount to install in its cargo hold.

    An installation fee will be deduced by the Shipyard for installing the mount on the ship.

    Args:
        ship_symbol (str):
        json_body (InstallMountInstallMountRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        InstallMountInstallMount201Response
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
    json_body: InstallMountInstallMountRequest,
) -> Response[InstallMountInstallMount201Response]:
    """Install Mount

     Install a mount on a ship.

    In order to install a mount, the ship must be docked and located in a waypoint that has a `Shipyard`
    trait. The ship also must have the mount to install in its cargo hold.

    An installation fee will be deduced by the Shipyard for installing the mount on the ship.

    Args:
        ship_symbol (str):
        json_body (InstallMountInstallMountRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[InstallMountInstallMount201Response]
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
    json_body: InstallMountInstallMountRequest,
) -> Optional[InstallMountInstallMount201Response]:
    """Install Mount

     Install a mount on a ship.

    In order to install a mount, the ship must be docked and located in a waypoint that has a `Shipyard`
    trait. The ship also must have the mount to install in its cargo hold.

    An installation fee will be deduced by the Shipyard for installing the mount on the ship.

    Args:
        ship_symbol (str):
        json_body (InstallMountInstallMountRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        InstallMountInstallMount201Response
    """

    return (
        await asyncio_detailed(
            ship_symbol=ship_symbol,
            client=client,
            json_body=json_body,
        )
    ).parsed
