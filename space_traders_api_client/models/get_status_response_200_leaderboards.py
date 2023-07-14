from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.get_status_response_200_leaderboards_most_credits_item import (
        GetStatusResponse200LeaderboardsMostCreditsItem,
    )
    from ..models.get_status_response_200_leaderboards_most_submitted_charts_item import (
        GetStatusResponse200LeaderboardsMostSubmittedChartsItem,
    )


T = TypeVar("T", bound="GetStatusResponse200Leaderboards")


@attr.s(auto_attribs=True)
class GetStatusResponse200Leaderboards:
    """
    Attributes:
        most_credits (List['GetStatusResponse200LeaderboardsMostCreditsItem']): Top agents with the most credits.
        most_submitted_charts (List['GetStatusResponse200LeaderboardsMostSubmittedChartsItem']): Top agents with the
            most charted submitted.
    """

    most_credits: List["GetStatusResponse200LeaderboardsMostCreditsItem"]
    most_submitted_charts: List["GetStatusResponse200LeaderboardsMostSubmittedChartsItem"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        most_credits = []
        for most_credits_item_data in self.most_credits:
            most_credits_item = most_credits_item_data.to_dict()

            most_credits.append(most_credits_item)

        most_submitted_charts = []
        for most_submitted_charts_item_data in self.most_submitted_charts:
            most_submitted_charts_item = most_submitted_charts_item_data.to_dict()

            most_submitted_charts.append(most_submitted_charts_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mostCredits": most_credits,
                "mostSubmittedCharts": most_submitted_charts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_status_response_200_leaderboards_most_credits_item import (
            GetStatusResponse200LeaderboardsMostCreditsItem,
        )
        from ..models.get_status_response_200_leaderboards_most_submitted_charts_item import (
            GetStatusResponse200LeaderboardsMostSubmittedChartsItem,
        )

        d = src_dict.copy()
        most_credits = []
        _most_credits = d.pop("mostCredits")
        for most_credits_item_data in _most_credits:
            most_credits_item = GetStatusResponse200LeaderboardsMostCreditsItem.from_dict(most_credits_item_data)

            most_credits.append(most_credits_item)

        most_submitted_charts = []
        _most_submitted_charts = d.pop("mostSubmittedCharts")
        for most_submitted_charts_item_data in _most_submitted_charts:
            most_submitted_charts_item = GetStatusResponse200LeaderboardsMostSubmittedChartsItem.from_dict(
                most_submitted_charts_item_data
            )

            most_submitted_charts.append(most_submitted_charts_item)

        get_status_response_200_leaderboards = cls(
            most_credits=most_credits,
            most_submitted_charts=most_submitted_charts,
        )

        get_status_response_200_leaderboards.additional_properties = d
        return get_status_response_200_leaderboards

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
