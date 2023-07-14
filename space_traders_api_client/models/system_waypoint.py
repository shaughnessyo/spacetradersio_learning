from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.waypoint_type import WaypointType

T = TypeVar("T", bound="SystemWaypoint")


@attr.s(auto_attribs=True)
class SystemWaypoint:
    """
    Attributes:
        symbol (str): The symbol of the waypoint.
        type (WaypointType): The type of waypoint.
        x (int): Position in the universe in the x axis.
        y (int): Position in the universe in the y axis.
    """

    symbol: str
    type: WaypointType
    x: int
    y: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        symbol = self.symbol
        type = self.type.value

        x = self.x
        y = self.y

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "symbol": symbol,
                "type": type,
                "x": x,
                "y": y,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        symbol = d.pop("symbol")

        type = WaypointType(d.pop("type"))

        x = d.pop("x")

        y = d.pop("y")

        system_waypoint = cls(
            symbol=symbol,
            type=type,
            x=x,
            y=y,
        )

        system_waypoint.additional_properties = d
        return system_waypoint

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
