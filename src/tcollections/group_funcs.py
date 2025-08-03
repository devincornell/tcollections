from __future__ import annotations
import typing
import dataclasses
import collections

from .grouped_dict import GroupedDict
from .grouped_iter import GroupedIter

def groupby(iterable: typing.Iterable[T], key: typing.Callable[[T], K]) -> GroupedIter[K,T]:
    '''Group items from a collection by a key function.
    Args:
        iterable: The collection to group.
        key: A function that returns the key to group by.
    Returns:
        A dictionary subtype containing the items grouped by key.
    '''
    return GroupedIter.group(iterable=iterable, key=key)

def groupby_dict(d: typing.Dict[U,T], key: typing.Callable[[T], K]) -> GroupedDict[K,U,T]:
    '''Group dictionary values by a key function, preserving the original keys within each group.
    Args:
        d: The dictionary to group.
        key: A function that returns the key to group by.
    Returns:
        A dictionary subtype containing the items grouped by key.
    '''
    return GroupedDict.group(d=d, key=key)


def main():
    groups = GroupedIter.group(
        range(10),
        lambda x: x % 2
    )
    print(groups)
    groups.agg(sum)

    groups = GroupedIter.group(
        {1: 'a', 2: 'b', 3: 'c', 4: 'd'}.items(),
        lambda kv: kv[0] % 2
    )
    print(groups)
    print(groups.agg(lambda els: sum([len(v) for k,v in els])))

    groups = GroupedIter.group(
        {1: 'a', 2: 'b', 3: 'c', 4: 'd'},
        lambda k: k % 2
    )
    print(groups)
    print(groups.agg(sum))

    groups = GroupedDict.group(
        {1: 'a', 2: 'b', 3: 'c', 4: 'd'},
        lambda x: len(x),
    )
    print(groups)
    print(groups.agg(lambda ds: sum(map(ord, ds.values()))))

if __name__ == '__main__':
    main()

