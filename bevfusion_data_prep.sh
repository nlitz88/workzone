#!/bin/bash

# run data preparation
python tools/create_data.py nuscenes --root-path data/nuscenes --out-dir data/nuscenes --extra-tag nuscenes --version v1.0-mini