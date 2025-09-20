from __future__ import annotations
from typing import TypeVar, Protocol, Iterator, Union, runtime_checkable, Self, Any
from collections.abc import Callable, Iterable, Hashable
from abc import ABC, abstractmethod
import typing  # Keep this for backward compatibility


T = TypeVar('T')
K = TypeVar('K', bound=Hashable)  # Keys must be hashable
V = TypeVar('V')
U = TypeVar('U')


@runtime_checkable
class GroupCollection(Protocol[T]):
    """Protocol defining what makes a collection groupable."""
    def agg(self, func: Callable[[T], V]) -> V: ...


class GroupsBase(dict[K, Self|GroupCollection[T]]):
    """Abstract base class for grouped collections with shared implementation."""

    @classmethod
    def from_dict(cls, d: dict[K, Iterable[T]], collection_type: typing.Type[GroupCollection[T]]) -> typing.Self:
        """Create a Groups instance from a standard dictionary."""
        result = {}
        for k, v in d.items():
            if isinstance(v, dict):
                result[k] = cls.from_dict(v, collection_type)
            else:
                result[k] = collection_type(v)
        return cls(result)
    
    def agg(self, func: Callable[[GroupCollection[T]], V]) -> dict[K, V]:
        """Aggregate each group using the provided function."""
        return {k: v.agg(func) for k, v in self.items()}
    
    def to_dict(self, collection_type: typing.Type[GroupCollection[T]]) -> dict[K, typing.Self|GroupCollection[T]]:
        """Convert the grouped collection to a standard dictionary."""
        return {k: dict(v.to_dict()) if isinstance(v,self.__class__) else collection_type(v) for k, v in self.items()}
    
    def flatten(self, collection_type: typing.Type[GroupCollection[T]] = None) -> GroupCollection[T]:
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
                # It's a nested group, recurse into it
                for value in group_or_collection.values():
                    collect_elements(value)
            else:
                # It's a collection, add all its elements
                all_elements.extend(group_or_collection)
        
        # Start collection from this group
        for value in self.values():
            collect_elements(value)
        
        # Determine collection type if not provided
        if collection_type is None:
            # Find the first collection to determine the type
            def find_first_collection(group_or_collection):
                if isinstance(group_or_collection, GroupsBase):
                    for value in group_or_collection.values():
                        result = find_first_collection(value)
                        if result is not None:
                            return result
                else:
                    return type(group_or_collection)
                return None
            
            collection_type = find_first_collection(self)
            if collection_type is None:
                # Fallback to list if no collections found
                from .typed_collections import tlist
                collection_type = tlist
        
        return collection_type(all_elements)
    
    def __repr__(self) -> str:
        """String representation of the grouped collection."""
        return f'{self.__class__.__name__}({dict(self)})'

class Groups(GroupsBase[T]):
    @classmethod
    def from_dict(cls, d: dict[K, Iterable[T]], collection_type: typing.Type[GroupCollection[T]]) -> Groups[T]:
        """Create a Groups instance from a standard dictionary."""
        return cls({k: collection_type(v) for k, v in d.items()})
        

class NestedGroups(GroupsBase[T]):
    """Abstract base class for grouped collections with shared implementation."""

    @classmethod
    def from_dict(cls, d: dict[K, Iterable[T]], collection_type: typing.Type[GroupCollection[T]]) -> Groups[T]:
        """Create a Groups instance from a standard dictionary."""
        for k, v in d.items():
            if isinstance(v, dict):
                d[k] = cls.from_dict(v, collection_type)
            else:
                d[k] = collection_type(v)
        return cls(d)
    
