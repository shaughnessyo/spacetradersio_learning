from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from log_status_code import LogInformation
from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_survey_response_201 import CreateSurveyResponse201
from ...types import Response

log_information = LogInformation()

def _get_kwargs(
    ship_symbol: str,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/my/ships/{shipSymbol}/survey".format(client.base_url, shipSymbol=ship_symbol)
    log_information.set_api_endpoint(url)
    log_information.set_obj_symbol(ship_symbol)
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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[CreateSurveyResponse201]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = CreateSurveyResponse201.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[CreateSurveyResponse201]:
    log_information.set_status_code(response.status_code)

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
) -> Response[CreateSurveyResponse201]:
    """Create Survey

     Create surveys on a waypoint that can be extracted such as asteroid fields. A survey focuses on
    specific types of deposits from the extracted location. When ships extract using this survey, they
    are guaranteed to procure a high amount of one of the goods in the survey.

    In order to use a survey, send the entire survey details in the body of the extract request.

    Each survey may have multiple deposits, and if a symbol shows up more than once, that indicates a
    higher chance of extracting that resource.

    Your ship will enter a cooldown after surveying in which it is unable to perform certain actions.
    Surveys will eventually expire after a period of time or will be exhausted after being extracted
    several times based on the survey's size. Multiple ships can use the same survey for extraction.

    A ship must have the `Surveyor` mount installed in order to use this function.

    Args:
        ship_symbol (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateSurveyResponse201]
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
) -> Optional[CreateSurveyResponse201]:
    """Create Survey

     Create surveys on a waypoint that can be extracted such as asteroid fields. A survey focuses on
    specific types of deposits from the extracted location. When ships extract using this survey, they
    are guaranteed to procure a high amount of one of the goods in the survey.

    In order to use a survey, send the entire survey details in the body of the extract request.

    Each survey may have multiple deposits, and if a symbol shows up more than once, that indicates a
    higher chance of extracting that resource.

    Your ship will enter a cooldown after surveying in which it is unable to perform certain actions.
    Surveys will eventually expire after a period of time or will be exhausted after being extracted
    several times based on the survey's size. Multiple ships can use the same survey for extraction.

    A ship must have the `Surveyor` mount installed in order to use this function.

    Args:
        ship_symbol (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateSurveyResponse201
    """

    return sync_detailed(
        ship_symbol=ship_symbol,
        client=client,
    ).parsed


async def asyncio_detailed(
    ship_symbol: str,
    *,
    client: AuthenticatedClient,
) -> Response[CreateSurveyResponse201]:
    """Create Survey

     Create surveys on a waypoint that can be extracted such as asteroid fields. A survey focuses on
    specific types of deposits from the extracted location. When ships extract using this survey, they
    are guaranteed to procure a high amount of one of the goods in the survey.

    In order to use a survey, send the entire survey details in the body of the extract request.

    Each survey may have multiple deposits, and if a symbol shows up more than once, that indicates a
    higher chance of extracting that resource.

    Your ship will enter a cooldown after surveying in which it is unable to perform certain actions.
    Surveys will eventually expire after a period of time or will be exhausted after being extracted
    several times based on the survey's size. Multiple ships can use the same survey for extraction.

    A ship must have the `Surveyor` mount installed in order to use this function.

    Args:
        ship_symbol (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateSurveyResponse201]
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
) -> Optional[CreateSurveyResponse201]:
    """Create Survey

     Create surveys on a waypoint that can be extracted such as asteroid fields. A survey focuses on
    specific types of deposits from the extracted location. When ships extract using this survey, they
    are guaranteed to procure a high amount of one of the goods in the survey.

    In order to use a survey, send the entire survey details in the body of the extract request.

    Each survey may have multiple deposits, and if a symbol shows up more than once, that indicates a
    higher chance of extracting that resource.

    Your ship will enter a cooldown after surveying in which it is unable to perform certain actions.
    Surveys will eventually expire after a period of time or will be exhausted after being extracted
    several times based on the survey's size. Multiple ships can use the same survey for extraction.

    A ship must have the `Surveyor` mount installed in order to use this function.

    Args:
        ship_symbol (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateSurveyResponse201
    """

    return (
        await asyncio_detailed(
            ship_symbol=ship_symbol,
            client=client,
        )
    ).parsed
