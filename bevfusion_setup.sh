#!/bin/bash

# run python setup
python setup.py develop &&

# fetch pretrained models
./tools/download_pretrained.sh
