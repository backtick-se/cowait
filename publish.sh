#!/bin/bash
cd "${0%/*}" || exit
set -e

if [ -z "$PYPI_TOKEN" ]; then
    echo "Error: PYPI_TOKEN not set"
    exit 1
fi

echo "Cleaning dist/ directory"
rm -rf ./dist/*

echo "Building package..."
python3 setup.py sdist bdist_wheel

echo "Publishing package..."
python3 -m twine upload \
    --username __token__ \
    --password $PYPI_TOKEN \
    dist/*

echo "Done!"
