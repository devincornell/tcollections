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


class Groups(dict[K, typing.Self|GroupCollection[T]]):
    """Abstract base class for grouped collections with shared implementation."""
    
    def agg(self, func: Callable[[GroupCollection[T]], V]) -> dict[K, V]:
        """Aggregate each group using the provided function."""
        return {k: v.agg(func) for k, v in self.items()}
    
    def to_dict(self, collection_type: typing.Type[GroupCollection[T]] = list) -> dict[K, typing.Self|GroupCollection[T]]:
        """Convert the grouped collection to a standard dictionary."""
        return {k: dict(v.to_dict()) if isinstance(v,self.__class__) else collection_type(v) for k, v in self.items()}
    
    def __repr__(self) -> str:
        """String representation of the grouped collection."""
        return f'{self.__class__.__name__}({dict(self)})'

