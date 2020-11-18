#!/bin/bash

UPLOAD_URL=$1
if [[ -z "${PYPI_LOGIN}" ]] || [[ -z "${PYPI_PASSWORD}" ]]; then
    echo "Environment variables PYPI_LOGIN and PYPI_PASSWORD need to be set."
    exit 1
fi

echo "building distribution packages"
python setup.py sdist bdist_wheel
echo "publishing to ${UPLOAD_URL}"
python -m twine upload -u $PYPI_LOGIN -p $PYPI_PASSWORD --repository-url $UPLOAD_URL dist/*
