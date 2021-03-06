#!/bin/bash
set -e

# setup
python _check_setup.py
if [ $? -ne 0 ]; then
    echo 'Setup failed.'
    exit 1
fi

# pip install
PIP_REQUIREMENTS_FILE_PATH=`python _config.py PIP_REQUIREMENTS_FILE_PATH`
EXTRA_PYTHON_IMPORT_PATH=`python _config.py EXTRA_PYTHON_IMPORT_PATH`

if [ -f ${PIP_REQUIREMENTS_FILE_PATH} ]; then
    pip install -r ${PIP_REQUIREMENTS_FILE_PATH} --target ${EXTRA_PYTHON_IMPORT_PATH}
fi

# run worker
python _celery.py worker -A worker -l error -q $*
