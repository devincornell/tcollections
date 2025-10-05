# `tcollections`: Typed Collections

This package offers a set of collection and grouping types that are useful for data pipelines. The collections here offer a style that maintains the clarity and structure of traditional Python data structures while exposing a functional interface inspired by popular data science packages such as `pandas`.

## Installation

```bash
pip install tcollections
```

## Quick Start

```python
from tcollections import tlist, group

# Create a typed list
data = tlist([1, 2, 3, 4, 5])

# Group data
groups = group(data, key=lambda x: x % 2)
```

## Examples

See the examples in `examples/` for detailed usage examples:
- `01_introduction.ipynb` - Basic introduction to tcollections
- `02_data_analysis.ipynb` - Data analysis examples

## Features

- **Typed Collections**: `tlist` and `tset` with enhanced functionality
- **Grouping Operations**: Powerful grouping and aggregation functions
- **Functional Interface**: Clean, chainable operations
- **Data Pipeline Ready**: Designed for data processing workflows



