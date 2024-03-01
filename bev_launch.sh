#!/bin/bash

rocker --nvidia --x11 --name bevfusion --volume ../bevfusion/:/bevfusion/ -- workzone_boundary_project