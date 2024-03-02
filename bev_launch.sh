#!/bin/bash

# rocker --nvidia --x11 --name bevfusion --volume ../bevfusion/:/bevfusion/ -- workzone_boundary_project

# Update: Have to pass in the ipc=enable flag--which rocker does not natively
# support. This docker command will work temporarily--it's literally just the
# docker run command that the above rocker command produces, but with the
# ipc=host flag added. This isn't a good solution long term, however, as rocker
# does some steps prior to running this (like building a custom image with
# additional layers on top of the image you specify) that this doesn't do.

# THEREFORE, you can use this in the following way for now (until we just create
# our own dockerfile):
# 1. Run the above rocker command.
# 2. In the CLI output of the rocker command, you should be able to find the
#    docker run command that it calls under the hood (it will look similar to
#    the docker run command below).
# 3. Copy that docker run command, add the ipc=host flag into the command
#    (see below for an example), and then run it.

# Solution thread:
# https://github.com/ultralytics/yolov3/issues/283#issuecomment-552776535
# docker run --rm -it -v /etc/gitconfig:/etc/gitconfig:ro -v /home/nlitz88/.gitconfig:/home/None/.gitconfig:ro  --gpus all -e SSH_AUTH_SOCK -v /home/nlitz88/.byobu/.ssh-agent:/home/nlitz88/.byobu/.ssh-agent -v /home/nlitz88/repos/18744/workzone:/workzone  -e DISPLAY -e TERM   -e QT_X11_NO_MITSHM=1   -e XAUTHORITY=/tmp/.dockerf0au6zn2.xauth -v /tmp/.dockerf0au6zn2.xauth:/tmp/.dockerf0au6zn2.xauth   -v /tmp/.X11-unix:/tmp/.X11-unix   -v /etc/localtime:/etc/localtime:ro --ipc=host