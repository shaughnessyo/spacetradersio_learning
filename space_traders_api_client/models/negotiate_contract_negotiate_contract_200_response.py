from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.negotiate_contract_negotiate_contract_200_response_data import (
        NegotiateContractNegotiateContract200ResponseData,
    )


T = TypeVar("T", bound="NegotiateContractNegotiateContract200Response")


@attr.s(auto_attribs=True)
class NegotiateContractNegotiateContract200Response:
    """
    Attributes:
        data (NegotiateContractNegotiateContract200ResponseData):
    """

    data: "NegotiateContractNegotiateContract200ResponseData"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = self.data.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.negotiate_contract_negotiate_contract_200_response_data import (
            NegotiateContractNegotiateContract200ResponseData,
        )

        d = src_dict.copy()
        data = NegotiateContractNegotiateContract200ResponseData.from_dict(d.pop("data"))

        negotiate_contract_negotiate_contract_200_response = cls(
            data=data,
        )

        negotiate_contract_negotiate_contract_200_response.additional_properties = d
        return negotiate_contract_negotiate_contract_200_response

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
