from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_system_waypoints_response_200 import GetSystemWaypointsResponse200
from ...types import UNSET, Response, Unset

from log_status_code import LogInformation

log_information = LogInformation()
def _get_kwargs(
    system_symbol: str,
    *,
    client: AuthenticatedClient,
    page: Union[Unset, None, int] = 1,
    limit: Union[Unset, None, int] = 10,
) -> Dict[str, Any]:
    url = "{}/systems/{systemSymbol}/waypoints".format(client.base_url, systemSymbol=system_symbol)
    log_information.set_api_endpoint(url)
    log_information.set_obj_symbol(system_symbol)
    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["page"] = page

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[GetSystemWaypointsResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetSystemWaypointsResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[GetSystemWaypointsResponse200]:
    log_information.set_status_code(response.status_code)

    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    system_symbol: str,
    *,
    client: AuthenticatedClient,
    page: Union[Unset, None, int] = 1,
    limit: Union[Unset, None, int] = 10,
) -> Response[GetSystemWaypointsResponse200]:
    """List Waypoints in System

     Return a paginated list of all of the waypoints for a given system.

    If a waypoint is uncharted, it will return the `Uncharted` trait instead of its actual traits.

    Args:
        system_symbol (str):
        page (Union[Unset, None, int]):  Default: 1.
        limit (Union[Unset, None, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetSystemWaypointsResponse200]
    """

    kwargs = _get_kwargs(
        system_symbol=system_symbol,
        client=client,
        page=page,
        limit=limit,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    system_symbol: str,
    *,
    client: AuthenticatedClient,
    page: Union[Unset, None, int] = 1,
    limit: Union[Unset, None, int] = 10,
) -> Optional[GetSystemWaypointsResponse200]:
    """List Waypoints in System

     Return a paginated list of all of the waypoints for a given system.

    If a waypoint is uncharted, it will return the `Uncharted` trait instead of its actual traits.

    Args:
        system_symbol (str):
        page (Union[Unset, None, int]):  Default: 1.
        limit (Union[Unset, None, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetSystemWaypointsResponse200
    """

    return sync_detailed(
        system_symbol=system_symbol,
        client=client,
        page=page,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    system_symbol: str,
    *,
    client: AuthenticatedClient,
    page: Union[Unset, None, int] = 1,
    limit: Union[Unset, None, int] = 10,
) -> Response[GetSystemWaypointsResponse200]:
    """List Waypoints in System

     Return a paginated list of all of the waypoints for a given system.

    If a waypoint is uncharted, it will return the `Uncharted` trait instead of its actual traits.

    Args:
        system_symbol (str):
        page (Union[Unset, None, int]):  Default: 1.
        limit (Union[Unset, None, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetSystemWaypointsResponse200]
    """

    kwargs = _get_kwargs(
        system_symbol=system_symbol,
        client=client,
        page=page,
        limit=limit,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    system_symbol: str,
    *,
    client: AuthenticatedClient,
    page: Union[Unset, None, int] = 1,
    limit: Union[Unset, None, int] = 10,
) -> Optional[GetSystemWaypointsResponse200]:
    """List Waypoints in System

     Return a paginated list of all of the waypoints for a given system.

    If a waypoint is uncharted, it will return the `Uncharted` trait instead of its actual traits.

    Args:
        system_symbol (str):
        page (Union[Unset, None, int]):  Default: 1.
        limit (Union[Unset, None, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetSystemWaypointsResponse200
    """

    return (
        await asyncio_detailed(
            system_symbol=system_symbol,
            client=client,
            page=page,
            limit=limit,
        )
    ).parsed
