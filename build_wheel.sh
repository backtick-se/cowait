#!/bin/bash
cd "$(dirname "$0")"

python setup.py bdist_wheel
aws s3 sync dist s3://castle-data-science-pipeline-public/client