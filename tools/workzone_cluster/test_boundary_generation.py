"""Script where we invoke the boundary generation on all the construction images
we can find.
"""

from pathlib import Path

import cv2
import numpy as np

from tools.workzone_cluster.boundary_generation import display_image, process_image
from tools.workzone_cluster.find_construction_images import get_construction_images


if __name__ == "__main__":

    # 1. Find all the images from the viz directory that contain construction
    #    objects. This is done by looking at the LiDAR bev view. NOTE: This step
    #    should be eliminated eventually, as we shouldn't have to filter out
    #    images based on HSV values or anything like that--only doing that now
    #    because we don't have a clean interface to BEVFusion's output.
    viz_directory = Path(r"/workzone/viz/")
    construction_image_dicts = get_construction_images(viz_directory=viz_directory)
    
    # 2. Run barrier generation on each of these images LiDAR BEV image.
    for image_dict in construction_image_dicts:
        image_dict["workzone_mask"] = process_image(image_dict["lidar_image_data"], verbose=False)
        # display_image(image_dict["workzone_mask"])

        bev_horizontal = np.hstack((image_dict["lidar_image_data"], image_dict["workzone_mask"]))
        cam0_image = cv2.resize(cv2.imread(str(image_dict["camera-0"])), image_dict["workzone_mask"].shape[:2] )
        cam1_image = cv2.resize(cv2.imread(str(image_dict["camera-1"])), image_dict["workzone_mask"].shape[:2] )
        camera_horizontal = np.hstack((cam0_image, cam1_image))
        stack = np.vstack((camera_horizontal, bev_horizontal))
        display_image(bev_horizontal)

    # # 3. Display each image alongside its original image.
    # for image_dict in construction_image_dicts:
    #     bev_horizontal = np.hstack((image_dict["lidar_image_data"], image_dict["workzone_mask"]))
    #     print(bev_horizontal.size)
    #     cam0_image = cv2.resize(cv2.imread(str(image_dict["camera-0"])), image_dict["workzone_mask"].shape[:2] )
    #     cam1_image = cv2.resize(cv2.imread(str(image_dict["camera-1"])), image_dict["workzone_mask"].shape[:2] )
    #     camera_horizontal = np.hstack((cam0_image, cam1_image))

    #     print(camera_horizontal.size)
    #     stack = np.vstack((camera_horizontal, bev_horizontal))
    #     display_image(stack)