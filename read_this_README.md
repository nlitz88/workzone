# Slight maintenance

Steps:
- Download [nuScenes v1.0-mini dataset](https://www.nuscenes.org/nuscenes#download)

- Unzip it into bevfusion/data/nuscenes directory that looks like:

```
bevfusion
├── data
│   ├── nuscenes
│   │   ├── maps
│   │   ├── samples
│   │   ├── sweeps
│   │   ├── v1.0-mini
```

- Build the docker container in docker folder. For my case, I did:

```
cd docker
docker build -t workzone_boundary_project -f Dockerfile .
```

- Launch the docker container using the bev_launch.sh. For my case I used:

```
rocker --nvidia --x11 --name bevfusion --volume ../bevfusion/:/bevfusion/ -- workzone_boundary_project
```

- In container, run data_prep_test.sh:
```
./data_prep_test.sh
```
