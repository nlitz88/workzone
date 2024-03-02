#!/bin/bash

# test model using visualize.py
torchpack dist-run -np 8 python tools/visualize.py configs/nuscenes/det/transfusion/secfpn/camera+lidar/swint_v0p075/convfuser.yaml --split "train"