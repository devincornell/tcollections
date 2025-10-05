# tcollections

## Development Setup

```bash
git clone https://github.com/devincornell/tcollections.git
cd tcollections
pip install -e .[dev]
```

## Running Tests

```bash
pytest tests/
```

## Building for Release

```bash
# Clean previous builds
rm -rf dist/ build/ src/*.egg-info/

# Build package
python -m build

# Test locally
pip install dist/*.whl

# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Upload to PyPI (production)
twine upload dist/*
```

## Version Management

Update version in both:
- `pyproject.toml`
- `src/tcollections/__init__.py`