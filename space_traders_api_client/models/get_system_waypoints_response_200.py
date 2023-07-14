from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.meta import Meta
    from ..models.waypoint import Waypoint


T = TypeVar("T", bound="GetSystemWaypointsResponse200")


@attr.s(auto_attribs=True)
class GetSystemWaypointsResponse200:
    """
    Attributes:
        data (List['Waypoint']):
        meta (Meta): Meta details for pagination.
    """

    data: List["Waypoint"]
    meta: "Meta"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()

            data.append(data_item)

        meta = self.meta.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
                "meta": meta,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.meta import Meta
        from ..models.waypoint import Waypoint

        d = src_dict.copy()
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = Waypoint.from_dict(data_item_data)

            data.append(data_item)

        meta = Meta.from_dict(d.pop("meta"))

        get_system_waypoints_response_200 = cls(
            data=data,
            meta=meta,
        )

        get_system_waypoints_response_200.additional_properties = d
        return get_system_waypoints_response_200

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
