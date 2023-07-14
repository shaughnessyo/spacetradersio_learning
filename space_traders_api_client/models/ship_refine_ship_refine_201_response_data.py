from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.cooldown import Cooldown
    from ..models.ship_cargo import ShipCargo
    from ..models.ship_refine_ship_refine_201_response_data_consumed_item import (
        ShipRefineShipRefine201ResponseDataConsumedItem,
    )
    from ..models.ship_refine_ship_refine_201_response_data_produced_item import (
        ShipRefineShipRefine201ResponseDataProducedItem,
    )


T = TypeVar("T", bound="ShipRefineShipRefine201ResponseData")


@attr.s(auto_attribs=True)
class ShipRefineShipRefine201ResponseData:
    """
    Attributes:
        cargo (ShipCargo): Ship cargo details.
        cooldown (Cooldown): A cooldown is a period of time in which a ship cannot perform certain actions.
        produced (List['ShipRefineShipRefine201ResponseDataProducedItem']): Goods that were produced by this refining
            process.
        consumed (List['ShipRefineShipRefine201ResponseDataConsumedItem']): Goods that were consumed during this
            refining process.
    """

    cargo: "ShipCargo"
    cooldown: "Cooldown"
    produced: List["ShipRefineShipRefine201ResponseDataProducedItem"]
    consumed: List["ShipRefineShipRefine201ResponseDataConsumedItem"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cargo = self.cargo.to_dict()

        cooldown = self.cooldown.to_dict()

        produced = []
        for produced_item_data in self.produced:
            produced_item = produced_item_data.to_dict()

            produced.append(produced_item)

        consumed = []
        for consumed_item_data in self.consumed:
            consumed_item = consumed_item_data.to_dict()

            consumed.append(consumed_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cargo": cargo,
                "cooldown": cooldown,
                "produced": produced,
                "consumed": consumed,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.cooldown import Cooldown
        from ..models.ship_cargo import ShipCargo
        from ..models.ship_refine_ship_refine_201_response_data_consumed_item import (
            ShipRefineShipRefine201ResponseDataConsumedItem,
        )
        from ..models.ship_refine_ship_refine_201_response_data_produced_item import (
            ShipRefineShipRefine201ResponseDataProducedItem,
        )

        d = src_dict.copy()
        cargo = ShipCargo.from_dict(d.pop("cargo"))

        cooldown = Cooldown.from_dict(d.pop("cooldown"))

        produced = []
        _produced = d.pop("produced")
        for produced_item_data in _produced:
            produced_item = ShipRefineShipRefine201ResponseDataProducedItem.from_dict(produced_item_data)

            produced.append(produced_item)

        consumed = []
        _consumed = d.pop("consumed")
        for consumed_item_data in _consumed:
            consumed_item = ShipRefineShipRefine201ResponseDataConsumedItem.from_dict(consumed_item_data)

            consumed.append(consumed_item)

        ship_refine_ship_refine_201_response_data = cls(
            cargo=cargo,
            cooldown=cooldown,
            produced=produced,
            consumed=consumed,
        )

        ship_refine_ship_refine_201_response_data.additional_properties = d
        return ship_refine_ship_refine_201_response_data

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
