from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.cooldown import Cooldown
    from ..models.ship_nav import ShipNav


T = TypeVar("T", bound="JumpShipResponse200Data")


@attr.s(auto_attribs=True)
class JumpShipResponse200Data:
    """
    Attributes:
        cooldown (Cooldown): A cooldown is a period of time in which a ship cannot perform certain actions.
        nav (ShipNav): The navigation information of the ship.
    """

    cooldown: "Cooldown"
    nav: "ShipNav"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cooldown = self.cooldown.to_dict()

        nav = self.nav.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cooldown": cooldown,
                "nav": nav,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.cooldown import Cooldown
        from ..models.ship_nav import ShipNav

        d = src_dict.copy()
        cooldown = Cooldown.from_dict(d.pop("cooldown"))

        nav = ShipNav.from_dict(d.pop("nav"))

        jump_ship_response_200_data = cls(
            cooldown=cooldown,
            nav=nav,
        )

        jump_ship_response_200_data.additional_properties = d
        return jump_ship_response_200_data

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
