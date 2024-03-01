#!/bin/bash

# run python setup
python setup.py develop &&

# fetch pretrained models
./tools/download_pretrained.sh &&

# run data preparation
python tools/create_data.py nuscenes --root-path data/nuscenes --out-dir data/nuscenes --extra-tag nuscenes --version v1.0-mini &&

# test model using visualize.py
torchpack dist-run -np 8 python tools/visualize.py configs/nuscenes/det/transfusion/secfpn/camera+lidar/swint_v0p075/convfuser.yaml