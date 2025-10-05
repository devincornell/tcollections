from __future__ import annotations
import typing
import dataclasses
import collections
import abc
from typing import Any

from typing import TypeVar, Generic, Callable, Any
from collections.abc import Iterable, Hashable

#from .groups import CollectionGroup, NestedGroup, create_groups
from .group_funcs_lowlevel import (
    _groupby_multi, 
    _groupby,
)
from .groups import Groups, NestedGroups

if typing.TYPE_CHECKING:
    from .chain import ChainFunc



T = typing.TypeVar('T')
K = TypeVar('K', bound=Hashable)
V = typing.TypeVar('V')

class DEFAULT_VALUE_TYPE:
    '''A default value to use for optional arguments.'''
    pass

DEFAULT_VALUE = DEFAULT_VALUE_TYPE()


class TypedCollection(abc.ABC, typing.Generic[T]):
    '''Base class for typed collections.'''

    @abc.abstractmethod
    def __iter__(self) -> typing.Iterator[T]:
        '''All collections must be iterable.'''
        pass

    @property
    def group(self) -> Grouper[T]:
        '''Access grouping operations for this set.'''
        return Grouper(self)

    def map(self, func: abc.Callable[[T], V]) -> typing.Self[V]:
        '''Map a function over the list.'''
        return self.__class__(map(func, self))

    def filter(self, func: abc.Callable[[T], bool]) -> typing.Self:
        '''Filter the list by a function.'''
        return self.__class__(filter(func, self))

    def value_counts(self) -> collections.Counter[T]:
        '''Return a counter of the elements in the list.'''
        return collections.Counter(self)

    def copy(self) -> typing.Self:
        '''Return a shallow copy of the list.'''
        return self.__class__(self)
    
    def agg(self, func: typing.Callable[[typing.Self], V]) -> V:
        '''Aggregate the elements using a function.'''
        return func(self)
    
    def reduce(self, func: typing.Callable[[V,T], V], start: V, from_left: bool = True) -> T:
        '''Reduce the list using a function with a starting value.'''
        it = self if from_left else reversed(self)
        value = start
        for e in it:
            value = func(value, e)
        return value

    def __rshift__(self, chain_func: ChainFunc) -> typing.Self:
        '''Pipe the collection into a function or another collection.'''
        return chain_func(self)

    def __repr__(self):
        return f'{self.__class__.__name__}({super().__repr__()})'



class tlist(list[T], TypedCollection[T]):
    '''A list of elements with a homogenous type.'''
    
    def sort(self, key: typing.Callable[[T], typing.Any] = None, reverse: bool = False) -> typing.Self:
        '''Sort the list, returning a new list.'''
        return self.__class__(sorted(self, key = key, reverse = reverse))

    def reverse(self) -> typing.Self:
        '''Return a reversed version of the list. Overwrites list reverse, which executes in-place.'''
        return self.__class__(reversed(self))

    def to_set(self) -> 'tset[T]':
        '''Convert this tlist to a tset.'''
        return tset(self)

    def __add__(self, other: typing.Self) -> typing.Self:
        '''Concatenate two tlists.'''
        return self.__class__(super().__add__(other))
    
    def __sub__(self, other: typing.Self) -> typing.Self:
        '''Subtract two tlists.'''
        return self.__class__(super().__sub__(other))
    
    def __mul__(self, n: int) -> typing.Self:
        '''Multiply the list by an integer.'''
        return self.__class__(super().__mul__(n))
    


class tset(set[T], TypedCollection[T]):
    '''A set of elements with a homogenous type.'''

    def to_list(self) -> 'tlist[T]':
        '''Convert this tset to a tlist.'''
        return tlist(self)

    def __or__(self, other: typing.Self) -> typing.Self:
        '''Union of two sets.'''
        return self.__class__(super().__or__(other))
    
    def __and__(self, other: typing.Self) -> typing.Self:
        '''Intersection of two sets.'''
        return self.__class__(super().__and__(other))
    
    def __sub__(self, other: typing.Self) -> typing.Self:
        '''Difference of two sets.'''
        return self.__class__(super().__sub__(other))
    
    def __xor__(self, other: typing.Self) -> typing.Self:
        '''Symmetric difference of two sets.'''
        return self.__class__(super().__xor__(other))
    
class Grouper(Generic[T]):
    '''Handles grouping operations for collections through composition.'''
    
    def __init__(self, collection: Iterable[T]):
        self._collection = collection

    def multi(self, key_func: Callable[[T], tuple[K, ...]]) -> NestedGroups[T]:
        '''Group items from a collection by multiple keys using a single key function that returns a tuple of keys.'''
        result = _groupby_multi(self._collection, key_func)
        return NestedGroups.from_dict(result, tlist)

    def by(self, key_func: Callable[[T], K]) -> Groups[T, tlist[T]]:
        '''Group items from a collection by a single key using a key function.'''
        result = _groupby(self._collection, key_func)
        #return Groups({k: tlist(v) for k, v in result.items()})
        return Groups.from_dict(result, tlist)