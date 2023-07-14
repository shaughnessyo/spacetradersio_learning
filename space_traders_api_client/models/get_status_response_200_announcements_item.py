from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="GetStatusResponse200AnnouncementsItem")


@attr.s(auto_attribs=True)
class GetStatusResponse200AnnouncementsItem:
    """
    Attributes:
        title (str):
        body (str):
    """

    title: str
    body: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        title = self.title
        body = self.body

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "body": body,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        title = d.pop("title")

        body = d.pop("body")

        get_status_response_200_announcements_item = cls(
            title=title,
            body=body,
        )

        get_status_response_200_announcements_item.additional_properties = d
        return get_status_response_200_announcements_item

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
