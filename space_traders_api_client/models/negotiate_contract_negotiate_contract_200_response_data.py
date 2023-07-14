from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.contract import Contract


T = TypeVar("T", bound="NegotiateContractNegotiateContract200ResponseData")


@attr.s(auto_attribs=True)
class NegotiateContractNegotiateContract200ResponseData:
    """
    Attributes:
        contract (Contract): Contract details.
    """

    contract: "Contract"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        contract = self.contract.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "contract": contract,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.contract import Contract

        d = src_dict.copy()
        contract = Contract.from_dict(d.pop("contract"))

        negotiate_contract_negotiate_contract_200_response_data = cls(
            contract=contract,
        )

        negotiate_contract_negotiate_contract_200_response_data.additional_properties = d
        return negotiate_contract_negotiate_contract_200_response_data

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
