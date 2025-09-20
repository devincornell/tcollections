
import typing

import json

import tempfile

import deepdiff


import unittest
import pytest

import sys
sys.path.append('../src')
import tcollections

@pytest.mark.parametrize('iterable, keyfunc, grp_expected, aggfunc, agg_expected', [
    (
        range(10), 
        lambda x: x % 2, 
        {0: [0, 2, 4, 6, 8], 1: [1, 3, 5, 7, 9]}, 
        sum, 
        {0: 20, 1: 25}
    ),
    (
        {1: 'a', 2: 'b', 3: 'c', 4: 'd'}.items(), 
        lambda kv: kv[0] % 2, 
        {1: [(1, 'a'), (3, 'c')], 0: [(2, 'b'), (4, 'd')]}, 
        lambda els: sum([len(v) for k,v in els]), 
        {1: 2, 0: 2}
    ),
])
def test_groupby_param(iterable, keyfunc, grp_expected, aggfunc, agg_expected):
    groups = tcollections.groupby(
        iterable,
        keyfunc,
    )
    #print(groups)
    assert groups.as_dict() == grp_expected
    assert groups.agg(aggfunc) == agg_expected

def test_groupby_set():
    groups = tcollections.groupby_set(
        list(range(3)) + list(range(5)),
        lambda x: x % 2,
    )
    assert groups.as_dict() == {0: {0, 2, 4}, 1: {1, 3}}

def test_groupby_dict():
    groups = tcollections.GroupedDict.from_dict(
        {1: 'a', 2: 'b', 3: 'c', 4: 'def', 16: 'fu', 17: 'fur', 18: 'furr', 19: 'furrr'},
        lambda v: len(v),
    )
    #print(groups)
    assert groups.as_dict() == {1: {1: 'a', 2: 'b', 3: 'c'}, 3: {4: 'def', 17: 'fur'}, 2: {16: 'fu'}, 4: {18: 'furr'}, 5: {19: 'furrr'}}


def test_groupby_base():
    elements = ['abc', 'abcd', 'abb', 'abbc', 'adfg', 'bcdf']

    groups = tcollections._groupby(elements, lambda x: len(x))
    assert(set(groups.keys()) == {3, 4})
    assert(set(groups[3]) == {'abc', 'abb'})
    assert(set(groups[4]) == {'abcd', 'abbc', 'adfg', 'bcdf'})
    
    groups = tcollections._groupby(elements, lambda x: len(x))

    print(f'test_groupby_base passed!')



def test_groupby_multi_base():
    elements = ['abc', 'abcd', 'abb', 'abbc', 'adfg', 'bcdf']
    keys = lambda x: (x[0], x[1], x[2])  # Group by first three characters
    groups = tcollections._groupby_multi(elements, keys)
    expected = {
        'a': {
            'b': {
                'c': ['abc', 'abcd'],
                'b': ['abb', 'abbc'],
            },
            'd': {
                'f': ['adfg'],
            },
        },
        'b': {
            'c': {
                'd': ['bcdf'],
            },
        },
    }
    #print(json.dumps(groups, indent=2))
    diff = deepdiff.DeepDiff(groups, expected, ignore_type_subclasses=True)#ignore_order=True)
    assert len(diff) == 0

    #groups = tcollections.groupby_multi(elements, keys)
    #diff = deepdiff.DeepDiff(groups, expected, ignore_type_subclasses=True)#ignore_order=True)
    #print(diff)
    #assert len(diff) == 0

    print(f'test_groupby_multi_base passed!')





if __name__ == '__main__':
    test_groupby_base()
    test_groupby_multi_base()

