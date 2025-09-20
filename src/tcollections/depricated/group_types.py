from __future__ import annotations
from typing import TypeVar, Protocol, Iterator, Union, runtime_checkable, Self, Any
from collections.abc import Callable, Iterable, Hashable
from abc import ABC, abstractmethod
import typing  # Keep this for backward compatibility


T = TypeVar('T')
K = TypeVar('K', bound=Hashable)  # Keys must be hashable
V = TypeVar('V')
U = TypeVar('U')

CollectionType = Union[list[T], set[T]]

@runtime_checkable
class Groupable(Protocol[T]):
    """Protocol defining what makes a collection groupable."""
    def __iter__(self) -> Iterator[T]: ...
    def __len__(self) -> int: ...


class GroupedCollection(ABC, dict[K, Groupable[T]]):
    """Abstract base class for grouped collections with shared implementation."""
    
    @abstractmethod
    def agg(self, func: Callable[[Groupable[T]], V]) -> dict[K, V]:
        """Each collection type implements its own aggregation."""
        pass
    
    def as_dict(self) -> dict[K, Groupable[T]]:
        """Convert the grouped collection to a standard dictionary."""
        return dict(self)
    
    def __repr__(self) -> str:
        """String representation of the grouped collection."""
        return f'{self.__class__.__name__}({dict(self)})'


class GroupedList(GroupedCollection[K, list[T]]):
    '''A dictionary subtype containing lists of items grouped by key.'''
    
    @classmethod
    def from_iterable_multi(cls, iterable: Iterable[T], keys: list[Callable[[T], K]]) -> Self[T]:
        '''Group items from a collection by multiple key functions recursively.
        Args:
            iterable: The collection to group.
            keys: A list of functions that return the keys to group by.
        Returns:
            A dictionary subtype containing the items grouped by key.
        '''
        if len(keys) == 1:
            return cls.from_iterable(iterable, keys[0])
        else:
            print(f'keys: {keys}')
            groups = cls.from_iterable(iterable, keys[0])
            print(f'groups: {groups}')
            #GroupedDict.from_dict(groups, key=keys[0])
            #groups = cls.from_iterable_multi(iterable=iterable, keys=keys[1:])
            return {k:GroupedDict.from_dict(vs, key=keys[0]) for k,vs in groups.items()}

    @classmethod
    def from_iterable(cls, iterable: typing.Iterable[T], key: typing.Callable[[T], K], ctype: typing.Type[list] = list) -> 'typing.Self[T]':
        return cls(group_elements(
            iterable = iterable,
            key = key,
            ctype = ctype,
            insert_func = lambda c, e: c.append(e),
        ))

    def agg(self, func: typing.Callable[[list[T]], V]) -> dict[K,V]:
        '''Aggregate the grouped elements using the given function.'''
        return aggregate(self, func)
    
    def as_dict(self) -> dict[K,list[T]]:
        '''Convert the grouped list to a non-grouped dictionary.'''
        return dict(self)
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({dict(self)})'
    
        
class GroupedSet(GroupedCollection[K, set[T]]):
    '''A dictionary subtype containing sets of items grouped by key.'''
    
    @classmethod
    def from_iterable(cls, iterable: Iterable[T], key: Callable[[T], K], ctype: type[list] = list) -> Self[T]:
        return cls(group_elements(
            iterable = iterable,
            key = key,
            ctype = ctype,
            insert_func = lambda c, e: c.add(e),
        ))
    
    def agg(self, func: typing.Callable[[set[T]], V]) -> dict[K,V]:
        '''Aggregate the grouped elements using the given function.'''
        return aggregate(self, func)
    
    def as_dict(self) -> dict[K,set[T]]:
        '''Convert the grouped list to a non-grouped dictionary.'''
        return dict(self)
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({dict(self)})'


class GroupedDict(GroupedCollection[K, dict[U,T]]):
    '''A dictionary subtype containing dictionaries of items grouped by key.'''

    @classmethod
    def from_dict(cls, d: dict[U,T], key: typing.Callable[[T], K]) -> 'typing.Self[K,U,T]':
        '''Group dictionary values by a key function, preserving the original keys within each group.
        Args:
            d: The dictionary to group.
            key: A function that returns the key to group by.
        Returns:
            A dictionary subtype containing the items grouped by key.
        '''
        groups = {}
        for u_key, item in d.items():
            k = key(item)
            if k not in groups:
                groups[k] = {}
            groups[k][u_key] = item
        return cls(groups)

    def agg(self, func: typing.Callable[[dict[U,T]], V]) -> dict[K,V]:
        return {k: func(el_dict) for k, el_dict in self.items()}

    def as_dict(self) -> dict[K,set[T]]:
        '''Convert the grouped list to a non-grouped dictionary.'''
        return dict(self)
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({dict(self)})'


def aggregate(
    groups: GroupedList[K,T] | GroupedSet[K,T], 
    func: typing.Callable[[CollectionType[T]], V],
) -> dict[K,V]:
    '''Aggregate the grouped elements using the given function.'''
    return {k: func(elements) for k, elements in groups.items()}

def group_elements(
    iterable: Iterable[T], 
    key: Callable[[T], K], 
    ctype: type[CollectionType[T]], 
    insert_func: Callable[[CollectionType[T], T], None],
) -> dict[K,T]:
    '''Group items from a collection by a key function.'''
    groups = {}
    for item in iterable:
        k = key(item)
        if k not in groups:
            groups[k] = ctype()
        #groups[k] = insert_func(groups[k], item)
        insert_func(groups[k], item)
    return groups


class RecursiveDefaultDict(dict[K, Union['RecursiveDefaultDict[K, V]', V]]):
    '''A dictionary that recursively creates nested dictionary structures.
    
    Example:
        >>> d = RecursiveDefaultDict()
        >>> d['a']['b']['c'] = 1  # Creates all intermediate dictionaries automatically
        >>> d['x']['y']['z'] = 2  # Automatically creates nested structure
    '''
    def __missing__(self, key: K) -> 'RecursiveDefaultDict[K, V]':
        '''Create a new RecursiveDefaultDict when a key is missing.'''
        self[key] = RecursiveDefaultDict()
        return self[key]
    
    def __getitem__(self, key: K) -> Union['RecursiveDefaultDict[K, V]', V]:
        '''Get an item, creating a new RecursiveDefaultDict if the key doesn't exist.'''
        try:
            return super().__getitem__(key)
        except KeyError:
            return self.__missing__(key)

    def to_dict(self) -> dict[K, Union[dict, V]]:
        '''Convert the RecursiveDefaultDict to a regular dictionary.'''
        return {k: (v.to_dict() if isinstance(v, RecursiveDefaultDict) else dict(v)) for k, v in self.items()}
    