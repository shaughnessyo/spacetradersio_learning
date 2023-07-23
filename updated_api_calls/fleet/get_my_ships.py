from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_my_ships_response_200 import GetMyShipsResponse200
from ...types import UNSET, Response, Unset

from log_status_code import LogInformation

log_information = LogInformation()
def _get_kwargs(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, None, int] = 1,
    limit: Union[Unset, None, int] = 10,
) -> Dict[str, Any]:
    url = "{}/my/ships".format(client.base_url)
    log_information.set_api_endpoint(url)
    log_information.set_obj_symbol('None')
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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[GetMyShipsResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetMyShipsResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[GetMyShipsResponse200]:
    log_information.set_status_code(response.status_code)
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, None, int] = 1,
    limit: Union[Unset, None, int] = 10,
) -> Response[GetMyShipsResponse200]:
    """List Ships

     Return a paginated list of all of ships under your agent's ownership.

    Args:
        page (Union[Unset, None, int]):  Default: 1.
        limit (Union[Unset, None, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetMyShipsResponse200]
    """

    kwargs = _get_kwargs(
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
    *,
    client: AuthenticatedClient,
    page: Union[Unset, None, int] = 1,
    limit: Union[Unset, None, int] = 10,
) -> Optional[GetMyShipsResponse200]:
    """List Ships

     Return a paginated list of all of ships under your agent's ownership.

    Args:
        page (Union[Unset, None, int]):  Default: 1.
        limit (Union[Unset, None, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetMyShipsResponse200
    """

    return sync_detailed(
        client=client,
        page=page,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, None, int] = 1,
    limit: Union[Unset, None, int] = 10,
) -> Response[GetMyShipsResponse200]:
    """List Ships

     Return a paginated list of all of ships under your agent's ownership.

    Args:
        page (Union[Unset, None, int]):  Default: 1.
        limit (Union[Unset, None, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetMyShipsResponse200]
    """

    kwargs = _get_kwargs(
        client=client,
        page=page,
        limit=limit,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, None, int] = 1,
    limit: Union[Unset, None, int] = 10,
) -> Optional[GetMyShipsResponse200]:
    """List Ships

     Return a paginated list of all of ships under your agent's ownership.

    Args:
        page (Union[Unset, None, int]):  Default: 1.
        limit (Union[Unset, None, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetMyShipsResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            limit=limit,
        )
    ).parsed
