from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="RefuelShipJsonBody")


@attr.s(auto_attribs=True)
class RefuelShipJsonBody:
    """
    Attributes:
        units (Union[Unset, int]): The amount of fuel to fill in the ship's tanks. When not specified, the ship will be
            refueled to its maximum fuel capacity. If the amount specified is greater than the ship's remaining capacity,
            the ship will only be refueled to its maximum fuel capacity. The amount specified is not in market units but in
            ship fuel units. Example: 100.
    """

    units: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        units = self.units

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if units is not UNSET:
            field_dict["units"] = units

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        units = d.pop("units", UNSET)

        refuel_ship_json_body = cls(
            units=units,
        )

        refuel_ship_json_body.additional_properties = d
        return refuel_ship_json_body

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
