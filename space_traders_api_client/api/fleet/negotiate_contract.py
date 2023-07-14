from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.negotiate_contract_negotiate_contract_200_response import NegotiateContractNegotiateContract200Response
from ...types import Response


def _get_kwargs(
    ship_symbol: str,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/my/ships/{shipSymbol}/negotiate/contract".format(client.base_url, shipSymbol=ship_symbol)

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


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[NegotiateContractNegotiateContract200Response]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = NegotiateContractNegotiateContract200Response.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[NegotiateContractNegotiateContract200Response]:
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
) -> Response[NegotiateContractNegotiateContract200Response]:
    """Negotiate Contract

     Negotiate a new contract with the HQ.

    In order to negotiate a new contract, an agent must not have ongoing or offered contracts over the
    allowed maximum amount. Currently the maximum contracts an agent can have at a time is 1.

    Once a contract is negotiated, it is added to the list of contracts offered to the agent, which the
    agent can then accept.

    The ship must be present at a faction's HQ waypoint to negotiate a contract with that faction.

    Args:
        ship_symbol (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[NegotiateContractNegotiateContract200Response]
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
) -> Optional[NegotiateContractNegotiateContract200Response]:
    """Negotiate Contract

     Negotiate a new contract with the HQ.

    In order to negotiate a new contract, an agent must not have ongoing or offered contracts over the
    allowed maximum amount. Currently the maximum contracts an agent can have at a time is 1.

    Once a contract is negotiated, it is added to the list of contracts offered to the agent, which the
    agent can then accept.

    The ship must be present at a faction's HQ waypoint to negotiate a contract with that faction.

    Args:
        ship_symbol (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        NegotiateContractNegotiateContract200Response
    """

    return sync_detailed(
        ship_symbol=ship_symbol,
        client=client,
    ).parsed


async def asyncio_detailed(
    ship_symbol: str,
    *,
    client: AuthenticatedClient,
) -> Response[NegotiateContractNegotiateContract200Response]:
    """Negotiate Contract

     Negotiate a new contract with the HQ.

    In order to negotiate a new contract, an agent must not have ongoing or offered contracts over the
    allowed maximum amount. Currently the maximum contracts an agent can have at a time is 1.

    Once a contract is negotiated, it is added to the list of contracts offered to the agent, which the
    agent can then accept.

    The ship must be present at a faction's HQ waypoint to negotiate a contract with that faction.

    Args:
        ship_symbol (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[NegotiateContractNegotiateContract200Response]
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
) -> Optional[NegotiateContractNegotiateContract200Response]:
    """Negotiate Contract

     Negotiate a new contract with the HQ.

    In order to negotiate a new contract, an agent must not have ongoing or offered contracts over the
    allowed maximum amount. Currently the maximum contracts an agent can have at a time is 1.

    Once a contract is negotiated, it is added to the list of contracts offered to the agent, which the
    agent can then accept.

    The ship must be present at a faction's HQ waypoint to negotiate a contract with that faction.

    Args:
        ship_symbol (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        NegotiateContractNegotiateContract200Response
    """

    return (
        await asyncio_detailed(
            ship_symbol=ship_symbol,
            client=client,
        )
    ).parsed
