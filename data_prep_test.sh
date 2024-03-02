#!/bin/bash

# run python setup
./bevfusion_setup.sh &&

# run data preparation
./bevfusion_data_prep.sh &&

# test model using visualize.py
./bevfusion_visualize.sh

# UPDATE: Broke this script out into multiple, separate scripts so that data
# prep and setup doesn't have to run every single time. You'll need to run the
# first two scripts called here if it's your first time running in the
# container.