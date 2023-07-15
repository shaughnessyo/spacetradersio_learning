from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_agent_response_200 import GetAgentResponse200
from ...types import Response


def _get_kwargs(
    agent_symbol: str = "FEBA66",
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/agents/{agentSymbol}".format(client.base_url, agentSymbol=agent_symbol)

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[GetAgentResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetAgentResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[GetAgentResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    agent_symbol: str = "FEBA66",
    *,
    client: AuthenticatedClient,
) -> Response[GetAgentResponse200]:
    """Get Public Agent

     Fetch agent details.

    Args:
        agent_symbol (str):  Default: 'FEBA66'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetAgentResponse200]
    """

    kwargs = _get_kwargs(
        agent_symbol=agent_symbol,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    agent_symbol: str = "FEBA66",
    *,
    client: AuthenticatedClient,
) -> Optional[GetAgentResponse200]:
    """Get Public Agent

     Fetch agent details.

    Args:
        agent_symbol (str):  Default: 'FEBA66'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetAgentResponse200
    """

    return sync_detailed(
        agent_symbol=agent_symbol,
        client=client,
    ).parsed


async def asyncio_detailed(
    agent_symbol: str = "FEBA66",
    *,
    client: AuthenticatedClient,
) -> Response[GetAgentResponse200]:
    """Get Public Agent

     Fetch agent details.

    Args:
        agent_symbol (str):  Default: 'FEBA66'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetAgentResponse200]
    """

    kwargs = _get_kwargs(
        agent_symbol=agent_symbol,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    agent_symbol: str = "FEBA66",
    *,
    client: AuthenticatedClient,
) -> Optional[GetAgentResponse200]:
    """Get Public Agent

     Fetch agent details.

    Args:
        agent_symbol (str):  Default: 'FEBA66'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetAgentResponse200
    """

    return (
        await asyncio_detailed(
            agent_symbol=agent_symbol,
            client=client,
        )
    ).parsed
