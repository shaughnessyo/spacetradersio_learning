from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.trade_symbol import TradeSymbol

T = TypeVar("T", bound="ExtractionYield")


@attr.s(auto_attribs=True)
class ExtractionYield:
    """Yields from the extract operation.

    Attributes:
        symbol (TradeSymbol): The good's symbol.
        units (int): The number of units extracted that were placed into the ship's cargo hold.
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

        extraction_yield = cls(
            symbol=symbol,
            units=units,
        )

        extraction_yield.additional_properties = d
        return extraction_yield

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
