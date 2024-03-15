"""Script where we invoke the boundary generation on all the construction images
we can find.
"""

from pathlib import Path

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

    # 3. Display each image alongside its original image.
    for image_dict in construction_image_dicts:
        numpy_horizontal = np.hstack((image_dict["lidar_image_data"], image_dict["workzone_mask"]))
        display_image(numpy_horizontal)