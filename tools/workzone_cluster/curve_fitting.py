import os
from pathlib import Path
import random
from typing import Optional
import cv2
import numpy as np
from tqdm import tqdm

# global verbose flag
VFLAG = True

# number of images to test on
NUM_IMAGES = 10

# HSV threshold 1
HSV_THRES_1_LOW = np.array([102, 45, 100])
HSV_THRES_1_HIGH = np.array([108, 65, 160])

# HSV threshold 2
HSV_THRES_2_LOW = np.array([87, 90, 60])
HSV_THRES_2_HIGH = np.array([93, 115, 80])

def blur_image(input_image, verbose=VFLAG):
    
    # Apply Gaussian blur
    blurred_image = cv2.GaussianBlur(input_image, (5, 5), 0)
    
    return blurred_image

def threshold_image(input_image, verbose=VFLAG):
    
    # switch to hsv color scheme
    hsv_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)
    
    # apply the first mask
    mask_barrier = cv2.inRange(hsv_image, HSV_THRES_1_LOW, HSV_THRES_1_HIGH)
    
    # apply the second mask
    mask_cone = cv2.inRange(hsv_image, HSV_THRES_2_LOW, HSV_THRES_2_HIGH)
    
    # combine masks
    mask_combine = cv2.bitwise_or(mask_barrier, mask_cone)
    
    # apply mask
    masked_image = cv2.bitwise_and(input_image, input_image, mask=mask_combine)
    
    # convert to grayscale
    gray_image = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)
    
    # binarize image
    _, binary_image = cv2.threshold(gray_image, 10, 255, cv2.THRESH_BINARY)
        
    return binary_image

def find_connected_components(binary_image, verbose=VFLAG):
    # Find connected components
    analysis = cv2.connectedComponentsWithStats(binary_image, 8, cv2.CV_32S) 
    (num_labels, labels, values, centroid) = analysis

    # Create a color map for visualization
    label_hue = np.uint8(179 * labels / np.max(labels))
    blank_ch = 255 * np.ones_like(label_hue)
    labeled_image = cv2.merge([label_hue, blank_ch, blank_ch])

    # Convert to BGR color map
    labeled_image = cv2.cvtColor(labeled_image, cv2.COLOR_HSV2BGR)
    labeled_image[label_hue == 0] = 0  # Set background label to black

    return labeled_image, num_labels

def apply_morphological_closing(binary_image: np.ndarray) -> np.ndarray:

    # kernel = np.ones((80,80),np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(80,80))
    processed_image = cv2.dilate(binary_image, kernel, iterations=2)
    erosion_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(50,50))
    processed_image = cv2.erode(processed_image, erosion_kernel, iterations=3)
        
    return processed_image

# def display_images(folder_path, num_images=NUM_IMAGES):
#     # Get list of images in the folder
#     images = [f for f in os.listdir(folder_path) if f.endswith('.png')]

#     # Randomly select 10 images
#     selected_images = random.sample(images, min(num_images, len(images)))

#     # Process each image with tqdm progress bar
#     for img_file in tqdm(selected_images, desc="Displaying images", unit="image"):
#         img_path = os.path.join(folder_path, img_file)
#         img = cv2.imread(img_path)
        
#         # blur each image
#         blur_img = blur_image(img)
        
#         # mask each image
#         mask_img = threshold_image(blur_img)
        
#         # identify components
#         label_img, num_labels = find_connected_components(mask_img)
        
#     cv2.destroyAllWindows()

def process_image(image: np.ndarray, verbose=VFLAG) -> np.ndarray:
    """Function to apply a sequence of transformations/processing stages on the
    provided image.

    Args:
        image (np.ndarray): Image as numpy array with dimensions h,w,c. 

    Returns:
        np.ndarray: The image with all processing steps applied.
    """

    # blur each image
    blur_img = blur_image(image)
    if verbose:
        display_image(image=blur_img,
                      window_name="Blurred Image")
    
    # mask each image
    mask_img = threshold_image(blur_img)
    if verbose:
        display_image(image=mask_img,
                      window_name="Binary Image")
    
    # identify components
    # label_img, num_labels = find_connected_components(mask_img)

    # Apply morphological closing.
    closed_image = apply_morphological_closing(binary_image=mask_img)
    if verbose:
        display_image(image=closed_image,
                      window_name="Morphological Closing")
    
    return closed_image

def display_image(image: np.ndarray, 
                  window_name: Optional[str] = "Processed Image") -> None:
    # Define window size
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 800, 800)
    
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":

    image_directory = Path(r"/workzone/viz/lidar/")
    test_images = [
        r"1532402941797653-0cd661df01aa40c3bb3a773ba86f753a.png"
    ]
    
    # Open the above images.
    images = []
    for image_name in test_images:
        images.append(cv2.imread(str(image_directory/image_name)))

    # Process and display each image.
    for image in images:
        processed_image = process_image(image, verbose=False)
        display_image(processed_image)
        display_image(image)