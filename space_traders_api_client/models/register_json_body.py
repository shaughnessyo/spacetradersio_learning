from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.faction_symbols import FactionSymbols
from ..types import UNSET, Unset

T = TypeVar("T", bound="RegisterJsonBody")


@attr.s(auto_attribs=True)
class RegisterJsonBody:
    """
    Attributes:
        faction (FactionSymbols): The symbol of the faction.
        symbol (str): Your desired agent symbol. This will be a unique name used to represent your agent, and will be
            the prefix for your ships. Example: BADGER.
        email (Union[Unset, str]): Your email address. This is used if you reserved your call sign between resets.
    """

    faction: FactionSymbols
    symbol: str
    email: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        faction = self.faction.value

        symbol = self.symbol
        email = self.email

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "faction": faction,
                "symbol": symbol,
            }
        )
        if email is not UNSET:
            field_dict["email"] = email

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        faction = FactionSymbols(d.pop("faction"))

        symbol = d.pop("symbol")

        email = d.pop("email", UNSET)

        register_json_body = cls(
            faction=faction,
            symbol=symbol,
            email=email,
        )

        register_json_body.additional_properties = d
        return register_json_body

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
