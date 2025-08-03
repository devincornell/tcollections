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




def groupby_multi(iterable: Iterable[T], keys: list[Callable[[T], K]]) -> GroupedList[K,T] | GroupedDict[K,U,GroupedList[K,T]]:
    '''Group items from a collection by multiple key functions recursively.
    Args:
        iterable: The collection to group.
        keys: A list of functions that return the keys to group by.
    Returns:
        A dictionary subtype containing the items grouped by key.
    '''

    groups = GroupedList.from_iterable(iterable, keys[0])
    
    if len(keys) == 1: # base case
        return groups
    else:
        multi_groups = dict()
        for k,vs in groups.items():
            multi_groups[k] = groupby_multi(vs, keys[1:])
        return GroupedDict(multi_groups)


def groupby(iterable: Iterable[T], key: Callable[[T], K]) -> GroupedList[K,T]:
    '''Group items from a collection by a key function.
    Args:
        iterable: The collection to group.
        key: A function that returns the key to group by.
    Returns:
        A dictionary subtype containing the items grouped by key.
    '''
    return GroupedList.from_iterable(iterable=iterable, key=key)


def groupby_set(iterable: Iterable[T], key: Callable[[T], K]) -> GroupedSet[K,T]:
    '''Group items from a collection by a key function.
    Args:
        iterable: The collection to group.
        key: A function that returns the key to group by.
    Returns:
        A dictionary subtype containing the items grouped by key.
    '''
    return GroupedSet.from_iterable(iterable=iterable, key=key)


def groupby_dict(d: dict[U,T], key: typing.Callable[[T], K]) -> GroupedDict[K,U,T]:
    '''Group dictionary values by a key function, preserving the original keys within each group.
    Args:
        d: The dictionary to group.
        key: A function that returns the key to group by.
    Returns:
        A dictionary subtype containing the items grouped by key.
    '''
    return GroupedDict.from_dict(d=d, key=key)



