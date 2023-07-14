import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.contract_type import ContractType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.contract_terms import ContractTerms


T = TypeVar("T", bound="Contract")


@attr.s(auto_attribs=True)
class Contract:
    """Contract details.

    Attributes:
        id (str): ID of the contract.
        faction_symbol (str): The symbol of the faction that this contract is for.
        type (ContractType): Type of contract.
        terms (ContractTerms): The terms to fulfill the contract.
        accepted (bool): Whether the contract has been accepted by the agent
        fulfilled (bool): Whether the contract has been fulfilled
        expiration (datetime.datetime): Deprecated in favor of deadlineToAccept
        deadline_to_accept (Union[Unset, datetime.datetime]): The time at which the contract is no longer available to
            be accepted
    """

    id: str
    faction_symbol: str
    type: ContractType
    terms: "ContractTerms"
    expiration: datetime.datetime
    accepted: bool = False
    fulfilled: bool = False
    deadline_to_accept: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        faction_symbol = self.faction_symbol
        type = self.type.value

        terms = self.terms.to_dict()

        accepted = self.accepted
        fulfilled = self.fulfilled
        expiration = self.expiration.isoformat()

        deadline_to_accept: Union[Unset, str] = UNSET
        if not isinstance(self.deadline_to_accept, Unset):
            deadline_to_accept = self.deadline_to_accept.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "factionSymbol": faction_symbol,
                "type": type,
                "terms": terms,
                "accepted": accepted,
                "fulfilled": fulfilled,
                "expiration": expiration,
            }
        )
        if deadline_to_accept is not UNSET:
            field_dict["deadlineToAccept"] = deadline_to_accept

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.contract_terms import ContractTerms

        d = src_dict.copy()
        id = d.pop("id")

        faction_symbol = d.pop("factionSymbol")

        type = ContractType(d.pop("type"))

        terms = ContractTerms.from_dict(d.pop("terms"))

        accepted = d.pop("accepted")

        fulfilled = d.pop("fulfilled")

        expiration = isoparse(d.pop("expiration"))

        _deadline_to_accept = d.pop("deadlineToAccept", UNSET)
        deadline_to_accept: Union[Unset, datetime.datetime]
        if isinstance(_deadline_to_accept, Unset):
            deadline_to_accept = UNSET
        else:
            deadline_to_accept = isoparse(_deadline_to_accept)

        contract = cls(
            id=id,
            faction_symbol=faction_symbol,
            type=type,
            terms=terms,
            accepted=accepted,
            fulfilled=fulfilled,
            expiration=expiration,
            deadline_to_accept=deadline_to_accept,
        )

        contract.additional_properties = d
        return contract

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
