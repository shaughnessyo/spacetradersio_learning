from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.trade_symbol import TradeSymbol

T = TypeVar("T", bound="JettisonJsonBody")


@attr.s(auto_attribs=True)
class JettisonJsonBody:
    """
    Attributes:
        symbol (TradeSymbol): The good's symbol.
        units (int): Amount of units to jettison of this good.
    """

    symbol: TradeSymbol
    units: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        symbol = self.symbol.value

        units = self.units

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "symbol": symbol,
                "units": units,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        symbol = TradeSymbol(d.pop("symbol"))

        units = d.pop("units")

        jettison_json_body = cls(
            symbol=symbol,
            units=units,
        )

        jettison_json_body.additional_properties = d
        return jettison_json_body

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
