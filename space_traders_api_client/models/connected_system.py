from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.system_type import SystemType
from ..types import UNSET, Unset




T = TypeVar("T", bound="ConnectedSystem")


@attr.s(auto_attribs=True)
class ConnectedSystem:
    """
    Attributes:
        symbol (str): The symbol of the system.
        sector_symbol (str): The sector of this system.
        type (SystemType): The type of waypoint.
        x (int): Position in the universe in the x axis.
        y (int): Position in the universe in the y axis.
        distance (int): The distance of this system to the connected Jump Gate.
        faction_symbol (Union[Unset, str]): The symbol of the faction that owns the connected jump gate in the system.
    """

    symbol: str
    sector_symbol: str
    type: SystemType
    x: int
    y: int
    distance: int
    faction_symbol: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        symbol = self.symbol
        sector_symbol = self.sector_symbol
        type = self.type.value

        x = self.x
        y = self.y
        distance = self.distance
        faction_symbol = self.faction_symbol

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "symbol": symbol,
                "sectorSymbol": sector_symbol,
                "type": type,
                "x": x,
                "y": y,
                "distance": distance,
            }
        )
        if faction_symbol is not UNSET:
            field_dict["factionSymbol"] = faction_symbol

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        symbol = d.pop("symbol")

        sector_symbol = d.pop("sectorSymbol")

        type = SystemType(d.pop("type"))

        x = d.pop("x")

        y = d.pop("y")

        distance = d.pop("distance")

        faction_symbol = d.pop("factionSymbol", UNSET)

        connected_system = cls(
            symbol=symbol,
            sector_symbol=sector_symbol,
            type=type,
            x=x,
            y=y,
            distance=distance,
            faction_symbol=faction_symbol,
        )

        connected_system.additional_properties = d
        return connected_system

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


# connected_system = ConnectedSystem
#
#
# connected_system.from_dict()