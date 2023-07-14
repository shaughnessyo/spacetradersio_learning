from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.faction_symbols import FactionSymbols

T = TypeVar("T", bound="WaypointFaction")


@attr.s(auto_attribs=True)
class WaypointFaction:
    """The faction that controls the waypoint.

    Attributes:
        symbol (FactionSymbols): The symbol of the faction.
    """

    symbol: FactionSymbols
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        symbol = self.symbol.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "symbol": symbol,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        symbol = FactionSymbols(d.pop("symbol"))

        waypoint_faction = cls(
            symbol=symbol,
        )

        waypoint_faction.additional_properties = d
        return waypoint_faction

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
