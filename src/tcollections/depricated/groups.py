from __future__ import annotations
from typing import TypeVar, Generic, Protocol, Iterator, Union, runtime_checkable
from collections.abc import Callable, Iterable, Hashable, Mapping
from abc import ABC, abstractmethod

T = TypeVar('T')
K = TypeVar('K', bound=Hashable)
V = TypeVar('V')

@runtime_checkable
class Groupable(Protocol[T]):
    """Protocol defining what makes a collection groupable."""
    def __iter__(self) -> Iterator[T]: ...
    def __len__(self) -> int: ...


class GroupedItems(dict[K, V]):
    """
    Base group type that maps keys to any value type.
    This is the most generic group type and serves as the base for more specific groups.
    """
    def __init__(self, data: dict[K, V]):
        super().__init__(data)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({super().__repr__()})"
    
    def as_dict(self) -> dict[K, V]:
        return dict(self)


class GroupedCollections(GroupedItems[K, Groupable[T]]):
    """
    A group whose values are collections (TList or TSet instances).
    """
    def aggregate(self, func: Callable[[Groupable[T]], V]) -> Group[K, V]:
        """Apply an aggregation function to each collection in the group."""
        return Groups({k: func(v) for k, v in self.items()})


class NestedGroups(GroupedItems[K, GroupedItems[K, V]]):
    """
    A group whose values are themselves groups.
    Used for multi-level grouping operations.
    """
    def flatten(self) -> Groups[tuple[K, K], V]:
        """Flatten a nested group into a single-level group with tuple keys."""
        result = {}
        for k1, subgroup in self.items():
            for k2, v in subgroup.items():
                result[(k1, k2)] = v
        return Groups(result)


def create_groups(items: Iterable[T], keys: list[Callable[[T], K]]) -> Union[CollectionGroups[K, T], NestedGroups[K, T]]:
    """
    Create a grouped structure from an iterable and a list of key functions.
    If one key is provided, returns a CollectionGroup.
    If multiple keys are provided, returns a NestedGroup.
    """
    if not keys:
        raise ValueError("At least one key function must be provided")
        
    # First level grouping
    first_groups: dict[K, list[T]] = {}
    for item in items:
        key = keys[0](item)
        if key not in first_groups:
            first_groups[key] = []
        first_groups[key].append(item)
    
    # If only one key function, return CollectionGroup
    if len(keys) == 1:
        from .tlist import TList  # Import here to avoid circular imports
        return CollectionGroups({k: TList(v) for k, v in first_groups.items()})
    
    # For multiple keys, recursively create nested groups
    return NestedGroups({
        k: create_groups(v, keys[1:])
        for k, v in first_groups.items()
    })
