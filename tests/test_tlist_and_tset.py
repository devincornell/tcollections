
import typing

import json

import tempfile

import deepdiff


import unittest
import pytest

import sys
sys.path.append('../src')
import tcollections






def test_tlist():
    elements = tcollections.tlist(['abc', 'abcd', 'abb', 'abbc', 'adfg', 'bcdf'])
    assert(elements.map(lambda x: x.lower()) == elements)
    lowered = elements.map(lambda x: x.upper())
    assert(lowered == [e.upper() for e in elements])

    filtered = elements.filter(lambda x: x.startswith('a'))
    assert(filtered == [e for e in elements if e.startswith('a')])

    counts = elements.value_counts()
    assert(set(counts.values()) == {1})
    assert(set((elements + elements).value_counts().values()) == {2})
    
    els2 = elements.copy()
    els2.append('new')
    assert(len(els2) == len(elements) + 1)

    assert(len(elements) == elements.apply(len))

    n = elements.reduce(lambda acc, x: acc + len(x), start=0)
    assert(n == sum(len(x) for x in elements))
    s = elements.reduce(lambda cum, x: cum + x, start='')
    assert(s == ''.join(elements))

    assert(len((elements + elements).to_set()) == len(elements))

if __name__ == '__main__':
    test_tlist()

