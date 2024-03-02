#!/bin/bash

# Change ownership of conda installation. Might be a faster way of doing this,
# but this works for now. Should really do this (if at all) when building the
# Docker image.
sudo chown -R $(id -u -n):$(id -g -n) /opt/conda/lib/python3.8/
sudo chown -R $(id -u -n):$(id -g -n) ./mmdet3d.egg-info/

# run python setup
python setup.py develop &&

# fetch pretrained models
./tools/download_pretrained.sh
