from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.trade_symbol import TradeSymbol

T = TypeVar("T", bound="TradeGood")


@attr.s(auto_attribs=True)
class TradeGood:
    """A good that can be traded for other goods or currency.

    Attributes:
        symbol (TradeSymbol): The good's symbol.
        name (str): The name of the good.
        description (str): The description of the good.
    """

    symbol: TradeSymbol
    name: str
    description: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        symbol = self.symbol.value

        name = self.name
        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "symbol": symbol,
                "name": name,
                "description": description,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        symbol = TradeSymbol(d.pop("symbol"))

        name = d.pop("name")

        description = d.pop("description")

        trade_good = cls(
            symbol=symbol,
            name=name,
            description=description,
        )

        trade_good.additional_properties = d
        return trade_good

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
