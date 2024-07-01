# Solutions Builder CLI Development

## Updating Solutions Template to PyPi package management

Check out the Solutions Builder repo:

```
git clone https://github.com/GoogleCloudPlatform/solutions-builder
cd solutions-builder
```

### To development locally

```
poetry lock && poetry install
```

Bump a version

```
poetry version patch

# For a minor bump:
poetry version minor

# For a major bump:
poetry version major
```

Build package

```
poetry build
```

- If encountering any errors, run `poetry build -vvv` to troubleshoot.

### Test package upload to Test-PyPI

Publish to Test-PyPI:

```
poetry config repositories.test-pypi https://test.pypi.org/legacy/
poetry config pypi-token.test-pypi $TEST_PYPI_TOKEN
poetry build && poetry publish -r test-pypi

```

Install and test from Test-PyPI

```
pip install -U --index-url https://test.pypi.org/simple/ solutions-builder
```

### Publish to official PyPI

Publish to PyPI

```
poetry config pypi-token.pypi $PYPI_TOKEN
poetry build && poetry publish
```

Test with the published package:

```
pip install -U solutions-builder
```
