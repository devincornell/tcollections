
__version__ = "0.1.0"

from .group_funcs import (
    group,
    groupby_multi,
    groupby,
)
from .groups import (
    Groups,
    NestedGroups,
    GroupCollection,
)


#from .grouping import groupby, groupby_set, groupby_multi, groupby_dict, GroupedList, GroupedSet, GroupedDict
from .typed_collections import (
    tlist, 
    tset,
)
from .group_funcs_lowlevel import (
    _groupby_multi, 
    _groupby,
)

from . import chain

__all__ = [
    "group", "groupby_multi", "groupby",
    "Groups", "NestedGroups", "GroupCollection", 
    "tlist", "tset",
    "chain",
]

