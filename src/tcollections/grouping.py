from __future__ import annotations
import typing
import dataclasses
import collections


T = typing.TypeVar('T')
K = typing.TypeVar('K')
V = typing.TypeVar('V')
U = typing.TypeVar('U')

CollectionType = typing.Union[list[T], set[T]]


def groupby_multi(iterable: typing.Iterable[T], keys: list[typing.Callable[[T], K]]) -> GroupedList[K,T] | GroupedDict[K,U,GroupedList[K,T]]:
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


def groupby(iterable: typing.Iterable[T], key: typing.Callable[[T], K]) -> GroupedList[K,T]:
    '''Group items from a collection by a key function.
    Args:
        iterable: The collection to group.
        key: A function that returns the key to group by.
    Returns:
        A dictionary subtype containing the items grouped by key.
    '''
    return GroupedList.from_iterable(iterable=iterable, key=key)


def groupby_set(iterable: typing.Iterable[T], key: typing.Callable[[T], K]) -> GroupedSet[K,T]:
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


#class GroupedCollection(dict[K,CollectionType[T]]):
#    '''A dictionary subtype containing lists of items grouped by key.'''
#    
#    def agg(self, func: typing.Callable[[CollectionType[T]], V]) -> dict[K,V]:
#        '''Aggregate the grouped elements using the given function.'''
#        return aggregate(self, func)
#    
#    def as_dict(self) -> dict[K,CollectionType[T]]:
#        '''Convert the grouped list to a non-grouped dictionary.'''
#        return dict(self)
#    
#    def __repr__(self) -> str:
#        return f'{self.__class__.__name__}({dict(self)})'


class GroupedList(dict[K,list[T]]):
    '''A dictionary subtype containing lists of items grouped by key.'''
    
    @classmethod
    def from_iterable_multi(cls, iterable: typing.Iterable[T], keys: list[typing.Callable[[T], K]]) -> 'typing.Self[T]':
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
    
        
class GroupedSet(dict[K,set[T]]):
    '''A dictionary subtype containing sets of items grouped by key.'''
    
    @classmethod
    def from_iterable(cls, iterable: typing.Iterable[T], key: typing.Callable[[T], K], ctype: typing.Type[list] = list) -> 'typing.Self[T]':
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


class GroupedDict(dict[K,dict[U,T]]):
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
    iterable: typing.Iterable[T], 
    key: typing.Callable[[T], K], 
    ctype: typing.Type[CollectionType[T]], 
    insert_func: typing.Callable[[CollectionType[T], T], None],
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
