
import typing
import dataclasses
import collections

from .typed_collections import TypedCollection
from .groups import Groups, NestedGroups, GroupCollection



T = typing.TypeVar('T')
V = typing.TypeVar('V')
K = typing.TypeVar('K', bound=typing.Hashable)  # Keys must be hashable


class ChainFunc:
    pass

@dataclasses.dataclass
class map(ChainFunc):
    '''Chain operator that maps a function over a typed collection.'''
    func: typing.Callable[[T], V]
    def __call__(self, collection: TypedCollection[T]) -> TypedCollection[V]:
        return collection.map(self.func)

@dataclasses.dataclass
class filter(ChainFunc):
    '''Chain operator that filters a typed collection.'''
    func: typing.Callable[[T], bool]

    def __call__(self, collection: TypedCollection[T]) -> TypedCollection[T]:
        return collection.filter(self.func)
    
@dataclasses.dataclass
class sort(ChainFunc):
    '''Chain operator that sorts a typed collection.'''
    reverse: bool = False
    def __call__(self, collection: TypedCollection[T]) -> TypedCollection[T]:
        return collection.sort(reverse=self.reverse)

@dataclasses.dataclass
class value_counts(ChainFunc):
    '''Chain operator that counts the elements in a typed collection.'''

    def __call__(self, collection: TypedCollection[T]) -> collections.Counter[T]:
        return collection.value_counts()
    
@dataclasses.dataclass
class size(ChainFunc):
    '''Chain operator that gets the size of a typed collection.'''

    def __call__(self, collection: TypedCollection[T]) -> int:
        return len(collection)

@dataclasses.dataclass
class chain_group_multi(ChainFunc):
    '''Chain operator that groups a typed collection by a key function.'''
    func: typing.Callable[[T], tuple[K, ...]]
    def __call__(self, collection: TypedCollection[T]) -> NestedGroups[K, GroupCollection[T]]:
        return collection.group.multi(self.func)

@dataclasses.dataclass
class chain_group_by(ChainFunc):
    '''Chain operator that groups a typed collection by a key function.'''
    func: typing.Callable[[T], K]
    def __call__(self, collection: TypedCollection[T]) -> Groups[K, GroupCollection[T]]:
        return collection.group.by(self.func)

class group:
    '''Contains static methods for grouping collections.'''
    @staticmethod
    def multi(key_func: typing.Callable[[T], tuple[K, ...]]) -> chain_group_multi:
        '''Chain operator to group items from a collection by multiple keys using a single key function that returns a tuple of keys.'''
        return chain_group_multi(key_func)

    @staticmethod
    def by(key_func: typing.Callable[[T], K]) -> chain_group_by:
        '''Chain operator to group items from a collection by a single key using a key function.'''
        return chain_group_by(key_func)
    
@dataclasses.dataclass
class aggregate(ChainFunc):
    '''Chain operator that aggregates a typed collection using a function.'''
    func: typing.Callable[[TypedCollection[T]], V]
    def __call__(self, groups: NestedGroups[K, GroupCollection[T]]|Groups[K, GroupCollection[T]]|TypedCollection[T]) -> dict[K, V]:
        return groups.agg(self.func)
