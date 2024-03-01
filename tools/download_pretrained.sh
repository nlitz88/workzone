#!/bin/bash
if [[ -d pretrained ]]; then
    exit
else
    mkdir pretrained &&
    cd pretrained &&
    wget https://hanlab18.mit.edu/projects/bevfusion/files/pretrained_updated/bevfusion-det.pth &&
    wget https://hanlab18.mit.edu/projects/bevfusion/files/pretrained_updated/bevfusion-seg.pth &&
    wget https://hanlab18.mit.edu/projects/bevfusion/files/pretrained/lidar-only-det.pth &&
    wget https://hanlab18.mit.edu/projects/bevfusion/files/pretrained/lidar-only-seg.pth &&
    wget https://hanlab18.mit.edu/projects/bevfusion/files/pretrained_updated/camera-only-det.pth &&
    wget https://hanlab18.mit.edu/projects/bevfusion/files/pretrained_updated/camera-only-seg.pth &&
    wget https://hanlab18.mit.edu/projects/bevfusion/files/pretrained_updated/swint-nuimages-pretrained.pth
fi
