# Solutions Builder Development

## Create a new Module

## Update the Template Root

## Updating Solutions Tempalte to PyPi package management

Check out the Solutions Builder repo:

```
git clone https://github.com/GoogleCloudPlatform/solutions-builder
cd solutions-builder
```

To development locally with editable files:
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
- If encountering any errors, run ```poetry build -vvv``` to troubleshoot.

Test package upload to Test-PyPI:
```
# Publish
poetry config repositories.test-pypi https://test.pypi.org/legacy/
poetry config pypi-token.test-pypi $PYPI_TOKEN
poetry publish -r test-pypi

# Install and test
python3 -m pip install --index-url https://test.pypi.org/simple/ solutions-builder
```

Publish to official PyPI:
```
# Publish to Test-PyPI
poetry config pypi-token.pypi $PYPI_TOKEN
poetry publish
```
