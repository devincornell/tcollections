from __future__ import annotations
from typing import TypeVar, Protocol, Iterator, Union, runtime_checkable, Self, Any
from collections.abc import Callable, Iterable, Hashable
from abc import ABC, abstractmethod
import typing  # Keep this for backward compatibility


T = TypeVar('T')
K = TypeVar('K', bound=Hashable)  # Keys must be hashable
V = TypeVar('V')
U = TypeVar('U')

from .group_funcs_lowlevel import _groupby, _groupby_multi
from .groups import Groups, NestedGroups
from .typed_collections import tlist, tset


def groupby_multi(iterable: Iterable[T], key_func: Callable[[T], tuple[K, ...]]) -> NestedGroups[T]:
    '''Group items from a collection by multiple keys using a single key function that returns a tuple of keys.'''
    result = _groupby_multi(iterable, key_func)
    return NestedGroups.from_dict(result, tlist)

def groupby(iterable: Iterable[T], key_func: Callable[[T], K]) -> Groups[T, tlist[T]]:
    '''Group items from a collection by a single key using a key function.'''
    result = _groupby(iterable, key_func)
    #return Groups({k: tlist(v) for k, v in result.items()})
    return Groups.from_dict(result, tlist)

