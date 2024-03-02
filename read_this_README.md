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

- Launch the docker container using the bev_launch.sh. **NOTE: See the
  bev_launch.sh script for updated notes on how to run the container. rocker
  won't work by itself due to some bug/requirement by bevfusion.**

```
rocker --nvidia --x11 --name bevfusion --volume ../bevfusion/:/bevfusion/ -- workzone_boundary_project
```

- In container, run data_prep_test.sh:
```
./data_prep_test.sh
```

### Filtering LiDAR BEV Output



1. To only visualize bounding boxes of construction-related objects: Comment out all entries in the `object_classes` section of
   `configs/nuscenes/default.yaml` so that it looks something like
   ```
   object_classes:
    # - car
    - truck
    - construction_vehicle
    # - bus
    # - trailer
    - barrier
    # - motorcycle
    # - bicycle
    # - pedestrian
    - traffic_cone
   ``` 
2. To remove white LiDAR points on BEV Map: Modify line `148` of `tools/visualize.py`
   to look something like this:
   ```
   if "points" in data:
    # lidar = data["points"].data[0][0].numpy()
    lidar = None   # Removes lidar visualization on BEV map.
    visualize_lidar(
        os.path.join(args.out_dir, "lidar", f"{name}.png"),
        lidar,
        bboxes=bboxes,
        labels=labels,
        xlim=[cfg.point_cloud_range[d] for d in [0, 3]],
        ylim=[cfg.point_cloud_range[d] for d in [1, 4]],
        classes=cfg.object_classes,
    )
   ```