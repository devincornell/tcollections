from __future__ import annotations
from typing import TypeVar, Generic, Callable, Any
from collections.abc import Iterable, Hashable

#from .groups import CollectionGroup, NestedGroup, create_groups

T = TypeVar('T')
K = TypeVar('K', bound=Hashable)

class Grouper(Generic[T]):
    """Handles grouping operations for collections through composition."""
    
    def __init__(self, collection: Iterable[T]):
        self._collection = collection
        
    #def by(self, key: Callable[[T], K]) -> CollectionGroup[K, T]:
    #    """
    #    Group the collection by a single key function.
    #    Always returns a CollectionGroup where values are list instances.
    #    """
    #    # Explicit single-key grouping
    #    groups: dict[K, list[T]] = {}
    #    for item in self._collection:
    #        k = key(item)
    #        if k not in groups:
    #            groups[k] = []
    #        groups[k].append(item)
    #        
    #    return CollectionGroup(groups)
            
    #def by_multi(self, *keys: Callable[[T], K]) -> CollectionGroup[K, T] | NestedGroup[K, T]:
    #    """
    #    Group the collection by multiple key functions.
    #    Returns:
    #        - CollectionGroup if one key is provided
    #        - NestedGroup if multiple keys are provided, where each level contains groups
    #    """
    #    if not keys:
    #        raise ValueError("At least one key function must be provided")
    #        
    #    if len(keys) == 1:
    #        return self.by(keys[0])
    #        
    #    return create_groups(self._collection, list(keys))
