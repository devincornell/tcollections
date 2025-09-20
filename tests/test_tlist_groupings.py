
import typing

import json

import tempfile

import deepdiff


import unittest
import pytest

import sys
sys.path.append('../src')
import tcollections


def test_tlist_groupings():
    elements = tcollections.tlist(['abc', 'abcd', 'abb', 'abbc', 'adfg', 'bcdf'])
    # finish this after building tests for groupby without tlist

if __name__ == '__main__':
    test_tlist_groupings()

