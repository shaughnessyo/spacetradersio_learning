from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.trade_symbol import TradeSymbol

T = TypeVar("T", bound="TransferCargoTransferCargoRequest")


@attr.s(auto_attribs=True)
class TransferCargoTransferCargoRequest:
    """
    Attributes:
        trade_symbol (TradeSymbol): The good's symbol.
        units (int): Amount of units to transfer.
        ship_symbol (str): The symbol of the ship to transfer to.
    """

    trade_symbol: TradeSymbol
    units: int
    ship_symbol: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        trade_symbol = self.trade_symbol.value

        units = self.units
        ship_symbol = self.ship_symbol

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tradeSymbol": trade_symbol,
                "units": units,
                "shipSymbol": ship_symbol,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        trade_symbol = TradeSymbol(d.pop("tradeSymbol"))

        units = d.pop("units")

        ship_symbol = d.pop("shipSymbol")

        transfer_cargo_transfer_cargo_request = cls(
            trade_symbol=trade_symbol,
            units=units,
            ship_symbol=ship_symbol,
        )

        transfer_cargo_transfer_cargo_request.additional_properties = d
        return transfer_cargo_transfer_cargo_request

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
