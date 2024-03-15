"""Script that is used to find images with construction object annotations or
predictions.
"""

import json
from pathlib import Path
from typing import List
import cv2
import numpy as np

from tools.workzone_cluster.boundary_generation import blur_image, display_image, threshold_image

def contains_construction_objects(image: np.ndarray) -> bool:
    """Determines whether an image contains construction objects or not based on
    the threshold_image function.

    NOTE: In the future, this function shouldn't be necessary, as we should have
    access to the class of each prediction output by BEVFusion.

    Args:
        image (np.ndarray): The BEV lidar image.

    Returns:
        bool: True if a construction object annotation/prediction is detected,
        false if not.
    """

    blur_img = blur_image(image)
    mask_img = threshold_image(blur_img)
    return np.sum(mask_img) > 0

def find_construction_images(image_directory: Path) -> List[np.ndarray]:
    """Searches through the provided image directory and finds images that have
    construction objects predictions or annotations.

    Args:
        image_directory (Path): The directory this function will look for images
        in. Note that this function does not recurse--it will only look at the
        directory you specify.

    Returns:
        List[np.ndarray]: Returns a list of images with construction objects.
        Specifically, returns a list of image dictionaries, where dictionary
        contains the file's filepath and image data.
    """

    # Iterate through all BEV images found in the specified directory.
    image_dicts = []
    for image_file in image_directory.iterdir():
        image_dict = {
            "lidar": str(image_file),
            "lidar_image_data": cv2.imread(str(image_file))
        }
        image_dicts.append(image_dict)

    construction_images = []
    for image_dict in image_dicts:
        if contains_construction_objects(image_dict["lidar_image_data"]):
            # display_image(image)
            construction_images.append(image_dict)

    print(f"Found {len(construction_images)} out of {len(image_dicts)} images with construction objects.")
    return construction_images

def get_corresponding_camera_frames(construction_image_dicts: List[dict],
                                    parent_dir: Path) -> List[dict]:

    # For a list of image dictionaries, grab the filepath of each of the
    # associated camera frames. They will have the same name, but will each be
    # in there own folder, specific to which camera they were captured on.

    for image_dict in construction_image_dicts:

        for camera_dir in parent_dir.iterdir():
            camera_name = str(camera_dir.parts[-1])
            if "camera" in camera_name:                
                image_dict[camera_name] = camera_dir/Path(image_dict["lidar"]).parts[-1]
    
    return construction_image_dicts

def get_construction_images(viz_directory: Path) -> List[dict]:
    """Returns a list of all the images in the provided BEVFusion visualization
    output directory that contain construction images. This is a wrapper for the
    above functions.

    Args:
        viz_directory (Path): The path to the output directory from BEVFusion's
        "visualize.py" script.

    Returns:
        List[dict]: A list of image dictionaries, where each dictionary contains
        the lidar image data and the filepaths to all the associated images
        (images from each camera and the LiDAR BEV view that the image data is
        from).
    """
    construction_image_dicts = find_construction_images(image_directory=viz_directory/"lidar")
    return get_corresponding_camera_frames(construction_image_dicts, viz_directory)

if __name__ == "__main__":

    viz_directory = Path(r"/workzone/viz/")
    get_construction_images(viz_directory=viz_directory)