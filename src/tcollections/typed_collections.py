from __future__ import annotations
import typing
import dataclasses
import collections
import abc
from typing import Any

from .grouper import Grouper


T = typing.TypeVar('T')
#K = typing.TypeVar('K')
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
        elements = list(self)
        ind_iter = range(len(elements)) if from_left else range(len(elements)-1, -1, -1)
        value = start
        for i in ind_iter:
            value = func(value, elements[i])
        return value

    def __repr__(self):
        return f'{self.__class__.__name__}({super().__repr__()})'



class TList(list[T], TypedCollection[T]):
    '''A list of elements with a homogenous type.'''

    def __init__(self, *args):
        super().__init__(*args)
        self._grouping = Grouper(self)
    
    @property
    def group(self) -> Grouper[T]:
        '''Access grouping operations for this list.'''
        return self._grouping
    
    def sort(self, key: typing.Callable[[T], typing.Any] = None, reverse: bool = False) -> typing.Self:
        '''Sort the list, returning a new list.'''
        return self.__class__(sorted(self, key = key, reverse = reverse))

    def reverse(self) -> typing.Self:
        '''Return a reversed version of the list. Overwrites list reverse, which executes in-place.'''
        return self.__class__(reversed(self))

    def to_set(self) -> 'TSet[T]':
        '''Convert this TList to a TSet.'''
        return TSet(self)

    def __add__(self, other: typing.Self) -> typing.Self:
        '''Concatenate two TLists.'''
        return self.__class__(super().__add__(other))
    
    def __sub__(self, other: typing.Self) -> typing.Self:
        '''Subtract two TLists.'''
        return self.__class__(super().__sub__(other))
    
    def __mul__(self, n: int) -> typing.Self:
        '''Multiply the list by an integer.'''
        return self.__class__(super().__mul__(n))
    


class TSet(set[T], TypedCollection[T]):
    '''A set of elements with a homogenous type.'''

    def __init__(self, *args):
        super().__init__(*args)
        self._grouping = Grouper(self)
    
    @property
    def group(self) -> Grouper[T]:
        '''Access grouping operations for this set.'''
        return self._grouping

    def to_list(self) -> 'TList[T]':
        '''Convert this TSet to a TList.'''
        return TList(self)

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
    
