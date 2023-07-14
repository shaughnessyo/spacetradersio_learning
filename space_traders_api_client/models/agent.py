from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="Agent")


@attr.s(auto_attribs=True)
class Agent:
    """Agent details.

    Attributes:
        account_id (str): Account ID that is tied to this agent.
        symbol (str): Symbol of the agent.
        headquarters (str): The headquarters of the agent.
        credits_ (int): The number of credits the agent has available. Credits can be negative if funds have been
            overdrawn.
        starting_faction (str): The faction the agent started with.
    """

    account_id: str
    symbol: str
    headquarters: str
    credits_: int
    starting_faction: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        account_id = self.account_id
        symbol = self.symbol
        headquarters = self.headquarters
        credits_ = self.credits_
        starting_faction = self.starting_faction

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accountId": account_id,
                "symbol": symbol,
                "headquarters": headquarters,
                "credits": credits_,
                "startingFaction": starting_faction,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        account_id = d.pop("accountId")

        symbol = d.pop("symbol")

        headquarters = d.pop("headquarters")

        credits_ = d.pop("credits")

        starting_faction = d.pop("startingFaction")

        agent = cls(
            account_id=account_id,
            symbol=symbol,
            headquarters=headquarters,
            credits_=credits_,
            starting_faction=starting_faction,
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
