from __future__ import annotations
from typing import TypeVar, Protocol, Iterator, Union, runtime_checkable, Self, Any
from collections.abc import Callable, Iterable, Hashable
from abc import ABC, abstractmethod
import typing  # Keep this for backward compatibility


T = TypeVar('T')
K = TypeVar('K', bound=Hashable)  # Keys must be hashable
V = TypeVar('V')
U = TypeVar('U')


def _groupby(iterable: Iterable[T], key_func: Callable[[T], K]) -> dict[K, list[T]]:
    '''Group items from a collection by a single key function.
    
    Args:
        iterable: The collection to group.
        key_func: A function that returns a key to group by.
    
    Returns:
        A dictionary where keys are the result of the key function and values are lists of elements that share the same key.
    
    Example:
        >>> items = ['apple', 'banana', 'cherry', 'date']
        >>> result = _groupby(items, lambda x: x[0])  # Group by first letter
        >>> # Result will be: {'a': ['apple'], 'b': ['banana'], 'c': ['cherry'], 'd': ['date']}
    '''
    result = {}
    
    for element in iterable:
        key = key_func(element)
        if key not in result:
            result[key] = []
        result[key].append(element)
    
    return result




def _groupby_multi(iterable: Iterable[T], key_func: Callable[[T], tuple[K, ...]]) -> dict[K,list[T]|dict[K,list[T]]]:
    '''Group items from a collection by multiple keys using a single key function that returns a tuple of keys.
    Creates a nested tree structure where each level corresponds to one key in the tuple.
    The leaf nodes contain lists of elements that share all the same keys.
    
    Args:
        iterable: The collection to group.
        key_func: A function that returns a tuple of keys to group by. The tuple order determines the nesting structure.
    
    Returns:
        A nested dictionary where each level represents grouping by one key from the tuple.
        The leaf nodes are lists containing the actual elements.
    
    Example:
        >>> items = [('A', 1), ('A', 2), ('B', 1), ('B', 2)]
        >>> result = groupby_multi(items, lambda x: x)  # x is already a tuple of (letter, number)
        >>> # Result will be: {'A': {1: [('A', 1)], 2: [('A', 2)]}, 'B': {1: [('B', 1)], 2: [('B', 2)]}}
    '''
    result = RecursiveDefaultDict()
    
    for element in iterable:
        current = result
        keys = key_func(element)
        
        # Navigate through all but the last key to build the nested structure
        for key in keys[:-1]:
            current = current[key]
        
        # For the last level, ensure we have a list of elements
        last_key = keys[-1]
        if last_key not in current:
            current[last_key] = []
        current[last_key].append(element)
    
    # Convert RecursiveDefaultDict to regular dict
    return result.to_dict()



class RecursiveDefaultDict(dict[K, Union['RecursiveDefaultDict[K, V]', V]]):
    '''A dictionary that recursively creates nested dictionary structures. Used to create tree-like structures.
    
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
        return self.to_type(dict, list)

    def to_type(self, dict_type: typing.Type[dict], value_type: typing.Type[V]) -> dict[K, Union[dict, V]]:
        '''Convert the RecursiveDefaultDict to a regular dictionary.'''
        return dict_type({k: (dict_type(v.to_type(dict_type, value_type)) if isinstance(v, self.__class__) else value_type(v)) for k, v in self.items()})


