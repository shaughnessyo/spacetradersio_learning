from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.agent import Agent
    from ..models.ship_cargo import ShipCargo
    from ..models.ship_modification_transaction import ShipModificationTransaction
    from ..models.ship_mount import ShipMount


T = TypeVar("T", bound="InstallMountInstallMount201ResponseData")


@attr.s(auto_attribs=True)
class InstallMountInstallMount201ResponseData:
    """
    Attributes:
        agent (Agent): Agent details.
        mounts (List['ShipMount']): List of installed mounts after the installation of the new mount.
        cargo (ShipCargo): Ship cargo details.
        transaction (ShipModificationTransaction): Result of a transaction for a ship modification, such as installing a
            mount or a module.
    """

    agent: "Agent"
    mounts: List["ShipMount"]
    cargo: "ShipCargo"
    transaction: "ShipModificationTransaction"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        agent = self.agent.to_dict()

        mounts = []
        for mounts_item_data in self.mounts:
            mounts_item = mounts_item_data.to_dict()

            mounts.append(mounts_item)

        cargo = self.cargo.to_dict()

        transaction = self.transaction.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "agent": agent,
                "mounts": mounts,
                "cargo": cargo,
                "transaction": transaction,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.agent import Agent
        from ..models.ship_cargo import ShipCargo
        from ..models.ship_modification_transaction import ShipModificationTransaction
        from ..models.ship_mount import ShipMount

        d = src_dict.copy()
        agent = Agent.from_dict(d.pop("agent"))

        mounts = []
        _mounts = d.pop("mounts")
        for mounts_item_data in _mounts:
            mounts_item = ShipMount.from_dict(mounts_item_data)

            mounts.append(mounts_item)

        cargo = ShipCargo.from_dict(d.pop("cargo"))

        transaction = ShipModificationTransaction.from_dict(d.pop("transaction"))

        install_mount_install_mount_201_response_data = cls(
            agent=agent,
            mounts=mounts,
            cargo=cargo,
            transaction=transaction,
        )

        install_mount_install_mount_201_response_data.additional_properties = d
        return install_mount_install_mount_201_response_data

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
