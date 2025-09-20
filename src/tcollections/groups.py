from __future__ import annotations
from typing import TypeVar, Protocol, Iterator, Union, runtime_checkable, Self, Any
from collections.abc import Callable, Iterable, Hashable
from abc import ABC, abstractmethod
import typing  # Keep this for backward compatibility
import json

T = TypeVar('T')
K = TypeVar('K', bound=Hashable)  # Keys must be hashable
V = TypeVar('V')
U = TypeVar('U')


@runtime_checkable
class GroupCollection(Protocol[T]):
    """Protocol defining what makes a collection groupable."""
    def __init__(self, iterable: Iterable[T]) -> None: ...
    def __iter__(self) -> Iterator[T]: ...
    def agg(self, func: Callable[[T], V]) -> V: ...


class GroupsBase(dict[K, Self|GroupCollection[T]]):
    """Abstract base class for grouped collections with shared implementation."""
    
    def agg(self, func: Callable[[GroupCollection[T]], V]) -> dict[K, V]:
        """Aggregate each group using the provided function."""
        return {k: v.agg(func) for k, v in self.items()}
    
    def to_dict(self, collection_type: typing.Type[GroupCollection[T]]|None = None) -> dict[K, typing.Self|GroupCollection[T]]:
        """Convert the grouped collection to a standard dictionary."""
        collection_type = collection_type or self.get_collection_type()
        return {k: dict(v.to_dict(collection_type)) if isinstance(v,self.__class__) else collection_type(v) for k, v in self.items()}
    
    
    def get_collection_type(self) -> typing.Type[GroupCollection[T]]:
        """Get the type of the collections stored in the groups."""
        for v in self.values():
            if isinstance(v, GroupsBase):
                return v.get_collection_type()
            else:
                return type(v)
        raise ValueError("No collections found in groups.")
    
    def __repr__(self) -> str:
        """String representation of the grouped collection."""
        return f'{self.__class__.__name__}({dict(self)})'
    
    def to_json(self, **kwargs) -> str:
        """Visualize the group structure."""
        # first, transform all of the dictionary keys to strings recursively
        def transform_keys(obj: Any) -> Any:
            if isinstance(obj, GroupsBase):
                return {str(k): transform_keys(v) for k, v in obj.items()}
            elif isinstance(obj, dict):
                return {str(k): transform_keys(v) for k, v in obj.items()}
            elif isinstance(obj, GroupCollection):
                return list(obj)
            else:
                return obj
        transformed = transform_keys(self)
        return json.dumps(transformed, **kwargs)

class Groups(GroupsBase[T]):
    '''Concrete class for grouped collections with shared implementation.'''
    @classmethod
    def from_dict(cls, d: dict[K, Iterable[T]], collection_type: typing.Type[GroupCollection[T]]) -> Groups[T]:
        """Create a Groups instance from a standard dictionary."""
        return cls({k: collection_type(v) for k, v in d.items()})

    def ungroup(self, collection_type: typing.Type[GroupCollection[T]] = None) -> GroupCollection[T]:
        """Alias for flatten to combine all elements into a single collection."""
        collection_type = collection_type or self.get_collection_type()
        return collection_type(item for group in self.values() for item in group)

class NestedGroups(GroupsBase[T]):
    '''Concrete class for nested grouped collections with shared implementation.'''

    @classmethod
    def from_dict(cls, d: dict[K, Iterable[T]], collection_type: typing.Type[GroupCollection[T]]) -> Groups[T]:
        """Create a Groups instance from a standard dictionary."""
        for k, v in d.items():
            if isinstance(v, dict):
                d[k] = cls.from_dict(v, collection_type)
            else:
                d[k] = collection_type(v)
        return cls(d)
    
    def flatten_other(self, collection_type: typing.Type[GroupCollection[T]] = None) -> GroupCollection[T]:
        """Flatten all grouped collections into a single collection, combining all elements.
        
        Args:
            collection_type: The type of collection to return. If None, defaults to the type 
                           of the first collection found in the groups.
        
        Returns:
            A single collection containing all elements from all groups.
        """
        all_elements = []
        
        # Recursively collect all elements
        def collect_elements(group_or_collection):
            if isinstance(group_or_collection, GroupsBase):
                for value in group_or_collection.values():
                    collect_elements(value)
            else:
                all_elements.extend(group_or_collection)
        
        # Start collection from this group
        for value in self.values():
            collect_elements(value)
        
        # Determine collection type if not provided
        if collection_type is None:
            collection_type = self.get_collection_type()
        
        return collection_type(all_elements)

    def ungroup(self, collection_type: typing.Type[GroupCollection[T]] = None) -> GroupCollection[T]:
        """Alias for flatten to combine all elements into a single collection."""
        collection_type = collection_type or self.get_collection_type()
        return collection_type(e for grps in self.flatten().values() for e in grps)

    def flatten(self) -> Groups[tuple, GroupCollection[T]]:
        '''Flatten the nested groups into a single grouping where keys are tuples of the original keys.'''
        flattened = Groups[tuple, GroupCollection[T]]()
        for key, group in self.items():
            if isinstance(group, NestedGroups):
                for sub_key, sub_value in group.flatten().items():
                    flattened[(key,) + sub_key] = sub_value
            else:
                flattened[(key,)] = group
        return flattened
