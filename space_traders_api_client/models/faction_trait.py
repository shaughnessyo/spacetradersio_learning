from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.faction_trait_symbol import FactionTraitSymbol

T = TypeVar("T", bound="FactionTrait")


@attr.s(auto_attribs=True)
class FactionTrait:
    """
    Attributes:
        symbol (FactionTraitSymbol): The unique identifier of the trait.
        name (str): The name of the trait.
        description (str): A description of the trait.
    """

    symbol: FactionTraitSymbol
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
        symbol = FactionTraitSymbol(d.pop("symbol"))

        name = d.pop("name")

        description = d.pop("description")

        faction_trait = cls(
            symbol=symbol,
            name=name,
            description=description,
        )

        faction_trait.additional_properties = d
        return faction_trait

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
