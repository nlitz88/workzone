"""Script that is used to find images with construction object annotations or
predictions.
"""

from pathlib import Path
from typing import List
import cv2
import numpy as np

from tools.workzone_cluster.curve_fitting import blur_image, display_image, threshold_image

def contains_construction_objects(image: np.ndarray) -> bool:

    blur_img = blur_image(image)
    mask_img = threshold_image(blur_img)
    return np.sum(mask_img) > 0

def find_construction_images(image_directory: Path) -> List[np.ndarray]:

    # Iterate through all BEV images found in the specified directory.
    image_dicts = []
    for image_file in bev_image_directory.iterdir():
        image_dict = {
            "filepath": str(image_file),
            "image_data": cv2.imread(str(image_file))
        }
        image_dicts.append(image_dict)

    construction_images = []
    for image_dict in image_dicts:
        if contains_construction_objects(image_dict["image_data"]):
            # display_image(image)
            construction_images.append(image_dict)

    print(f"Found {len(construction_images)} out of {len(image_dicts)} images with construction objects.")
    return construction_images

if __name__ == "__main__":

    bev_image_directory = Path(r"/workzone/viz/lidar/")
    find_construction_images(image_directory=bev_image_directory)