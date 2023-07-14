from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="InstallMountInstallMountRequest")


@attr.s(auto_attribs=True)
class InstallMountInstallMountRequest:
    """
    Attributes:
        symbol (str):
    """

    symbol: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        symbol = self.symbol

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "symbol": symbol,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        symbol = d.pop("symbol")

        install_mount_install_mount_request = cls(
            symbol=symbol,
        )

        install_mount_install_mount_request.additional_properties = d
        return install_mount_install_mount_request

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
