from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Agent")


@attr.s(auto_attribs=True)
class Agent:
    """Agent details.

    Attributes:
        symbol (str): Symbol of the agent.
        headquarters (str): The headquarters of the agent.
        credits_ (int): The number of credits the agent has available. Credits can be negative if funds have been
            overdrawn.
        starting_faction (str): The faction the agent started with.
        account_id (Union[Unset, str]): Account ID that is tied to this agent. Only included on your own agent.
        ship_count (Union[Unset, int]): How many ships are owned by the agent.
    """

    symbol: str
    headquarters: str
    credits_: int
    starting_faction: str
    account_id: Union[Unset, str] = UNSET
    ship_count: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        symbol = self.symbol
        headquarters = self.headquarters
        credits_ = self.credits_
        starting_faction = self.starting_faction
        account_id = self.account_id
        ship_count = self.ship_count

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "symbol": symbol,
                "headquarters": headquarters,
                "credits": credits_,
                "startingFaction": starting_faction,
            }
        )
        if account_id is not UNSET:
            field_dict["accountId"] = account_id
        if ship_count is not UNSET:
            field_dict["shipCount"] = ship_count

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        symbol = d.pop("symbol")

        headquarters = d.pop("headquarters")

        credits_ = d.pop("credits")

        starting_faction = d.pop("startingFaction")

        account_id = d.pop("accountId", UNSET)

        ship_count = d.pop("shipCount", UNSET)

        agent = cls(
            symbol=symbol,
            headquarters=headquarters,
            credits_=credits_,
            starting_faction=starting_faction,
            account_id=account_id,
            ship_count=ship_count,
        )

        agent.additional_properties = d
        return agent

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
