# Author: Ahmed Mohamed

from PIL import Image
import numpy as np
import os
import logging
import sys

# Set up logging
logging.basicConfig(filename='process.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define the directories (adjust as necessary)
input_dir = 'need_edit'
output_dir = 'edited'

# Determine the script directory
if getattr(sys, 'frozen', False):
    # The application is frozen by PyInstaller
    script_dir = os.path.dirname(sys.executable)
else:
    # The application is not frozen
    script_dir = os.path.dirname(os.path.abspath(__file__))

logging.debug(f"Script directory: {script_dir}")

# Create full paths for the input and output directories
input_dir_path = os.path.join(script_dir, input_dir)
output_dir_path = os.path.join(script_dir, output_dir)

logging.debug(f"Input directory path: {input_dir_path}")
logging.debug(f"Output directory path: {output_dir_path}")

# Ensure output directory exists
if not os.path.exists(output_dir_path):
    os.makedirs(output_dir_path)
    logging.debug(f"Created output directory: {output_dir_path}")

def process_image(input_path, output_path):
    logging.debug(f"Processing image: {input_path}")
    img = Image.open(input_path)
    img = img.convert('RGBA')  # Ensure image is in RGBA mode for transparency support
    logging.debug("Converted image to RGBA")

    # Perform basic background removal (example thresholding)
    img = remove_background_basic(img)
    logging.debug("Removed background")

    # Resize the image to 800x800 pixels using LANCZOS filter
    img_resized = img.resize((800, 800), Image.Resampling.LANCZOS)
    logging.debug("Resized image")

    # Save the edited image
    img_resized.save(output_path)
    logging.debug(f"Saved edited image: {output_path}")

def remove_background_basic(img):
    logging.debug("Removing background using basic thresholding")
    np_img = np.array(img)
    
    # Separate RGB channels and alpha channel
    r, g, b, a = np_img[:, :, 0], np_img[:, :, 1], np_img[:, :, 2], np_img[:, :, 3]
    
    # Calculate luminance (brightness) of each pixel
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    
    # Define a threshold for deciding what is background (adjust as needed)
    threshold = 180
    
    # Create a mask where pixels below the threshold are considered background
    mask = luminance < threshold
    
    # Invert the mask to keep object pixels
    mask = ~mask
    
    # Set background pixels to transparent
    np_img[mask, 3] = 0
    
    # Convert modified numpy array back to Image object
    img_modified = Image.fromarray(np_img)
    
    return img_modified

# Process all images in the input directory
if os.path.exists(input_dir_path):
    for filename in os.listdir(input_dir_path):
        input_path = os.path.join(input_dir_path, filename)
        output_path = os.path.join(output_dir_path, os.path.splitext(filename)[0] + '_edited.png')
        
        # Process the image if it is a file
        if os.path.isfile(input_path):
            try:
                process_image(input_path, output_path)
                logging.info(f"Processed and saved: {filename}")
            except Exception as e:
                logging.error(f"Error processing {filename}: {e}")
    
    logging.info(f"All images have been processed and saved to '{output_dir}'")
else:
    logging.error(f"Error: Input directory '{input_dir}' not found.")
