
import typing

import json

import tempfile

import deepdiff


import unittest
import pytest

import sys
sys.path.append('../src')
import tcollections
from tcollections import Groups, NestedGroups, GroupCollection, tlist

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
def ignore_test_groupby_param(iterable, keyfunc, grp_expected, aggfunc, agg_expected):
    groups = tcollections.groupby(
        iterable,
        keyfunc,
    )
    #print(groups)
    assert groups.as_dict() == grp_expected
    assert groups.agg(aggfunc) == agg_expected

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


def test_groups_flatten():
    """Test flatten method on Groups (single-level grouping)."""
    # Create some test data
    group_data = {
        'a': tlist([1, 2, 3]),
        'b': tlist([4, 5]),
        'c': tlist([6, 7, 8, 9])
    }
    
    groups = Groups(group_data)
    print(f"Original groups: {groups}")
    
    # Test flatten
    flattened = groups.flatten()
    print(f"Flattened: {flattened}")
    print(f"Flattened type: {type(flattened)}")
    
    # Verify all elements are present
    expected_elements = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert sorted(flattened) == sorted(expected_elements)
    assert isinstance(flattened, tlist)
    
    print("✓ Groups flatten test passed!")

def test_nested_groups_flatten():
    """Test flatten method on NestedGroups (multi-level grouping)."""
    # Create nested group data manually
    nested_data = {
        'x': {
            'a': tlist([1, 2]),
            'b': tlist([3, 4])
        },
        'y': {
            'c': tlist([5, 6]),
            'd': tlist([7, 8, 9])
        }
    }
    
    # Convert inner dicts to Groups instances
    nested_groups_data = {
        'x': Groups(nested_data['x']),
        'y': Groups(nested_data['y'])
    }
    
    nested_groups = NestedGroups(nested_groups_data)
    print(f"Original nested groups: {nested_groups}")
    
    # Test flatten
    flattened = nested_groups.flatten()
    print(f"Flattened nested: {flattened}")
    print(f"Flattened type: {type(flattened)}")
    
    # Verify all elements are present
    expected_elements = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert sorted(flattened) == sorted(expected_elements)
    assert isinstance(flattened, tlist)
    
    print("✓ NestedGroups flatten test passed!")


def test_flatten_with_groupby():
    """Test flatten method with the groupby function."""
    
    # Test with simple groupby
    data = list(range(10))
    groups = tcollections.groupby(data, lambda x: x % 3)
    print(f"Original grouped data: {groups}")
    
    flattened = groups.flatten()
    print(f"Flattened: {flattened}")
    
    # Should contain all original elements
    assert sorted(flattened) == sorted(data)
    print("✓ flatten with groupby test passed!")

def test_flatten_with_groupby_multi():
    """Test flatten method with multi-level grouping."""
    
    # Test with multi-level grouping
    data = ['abc', 'abd', 'aef', 'bcd', 'bef']
    
    # Group by first character, then second character
    groups = tcollections.groupby_multi(data, lambda x: (x[0], x[1]))
    print(f"Multi-level groups: {groups}")
    
    flattened = groups.flatten()
    print(f"Flattened multi-level: {flattened}")
    
    # Should contain all original elements
    assert sorted(flattened) == sorted(data)
    print("✓ flatten with groupby_multi test passed!")



if __name__ == '__main__':
    test_groupby_base()
    test_groupby_multi_base()

    test_groups_flatten()
    test_nested_groups_flatten()
    test_flatten_with_groupby()
    test_flatten_with_groupby_multi()
