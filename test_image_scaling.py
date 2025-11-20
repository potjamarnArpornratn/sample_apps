"""
Authored by: Potjamarn Arpornratn
Date: Nov 19, 2025

This script tests the image processing functions in image_scaling.py.
"""

import pytest
from PIL import Image
import os
import shutil
from image_scaling import process_images
import logging

logging.basicConfig(filename='test_image_scaling.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@pytest.fixture
def setup_test_images(tmp_path):
    """Create a set of test images in a temporary directory."""
    logger.info(f"Setting up test images in {tmp_path}")
    input_folder = tmp_path / "input_images"
    output_folder = tmp_path / "output_images"
    input_folder.mkdir(exist_ok=True)
    output_folder.mkdir(exist_ok=True)

    # Create test images
    colors = ["red", "green", "blue"]
    for i, color in enumerate(colors):
        logger.info(f"Creating test image {i} with color {color}")
        img = Image.new('RGB', (256, 256), color=color)
        img.save(input_folder / f"test_image_{i}.tif")

    return input_folder, output_folder

def test_process_images(setup_test_images):
    """Test the process_images function."""
    logger.info("Testing process_images function.")
    input_folder, output_folder = setup_test_images

    # Process the images
    process_images(str(input_folder), str(output_folder))

    # Verify that images are processed and saved correctly
    for filename in os.listdir(input_folder):
        logger.info(f"Verifying processed image for {filename}")
        base_filename = os.path.splitext(filename)[0]
        output_path = os.path.join(output_folder, f"{base_filename}.jpeg")
        assert os.path.exists(output_path), f"Processed image {output_path} does not exist."

        with Image.open(output_path) as img:
            # Check image size
            assert img.size == (128, 128), f"Image {output_path} has incorrect size {img.size}."
            # Check image format
            assert img.format == 'JPEG', f"Image {output_path} is not in JPEG format."

@pytest.fixture
def setup_test_images_with_invalid(tmp_path):
    """Create test images including an invalid file."""
    logger.info(f"Setting up test images with invalid file in {tmp_path}")
    input_folder = tmp_path / "input_images"
    output_folder = tmp_path / "output_images"
    input_folder.mkdir(exist_ok=True)
    output_folder.mkdir(exist_ok=True)

    # Create a valid image
    img = Image.new('RGB', (256, 256), color='red')
    img.save(input_folder / "valid_image.tif")

    # Create an invalid image file
    with open(input_folder / "invalid_image.tif", 'w') as f:
        f.write("This is not a valid image file.")

    return input_folder, output_folder

def test_process_images_with_invalid_file(setup_test_images_with_invalid):
    """Test the process_images function with an invalid image file."""
    logger.info("Testing process_images with invalid file.")
    input_folder, output_folder = setup_test_images_with_invalid

    # Process the images
    process_images(str(input_folder), str(output_folder))

    # Verify that only the valid image is processed
    valid_output_path = os.path.join(output_folder, "valid_image.jpeg")
    invalid_output_path = os.path.join(output_folder, "invalid_image.jpeg")

    assert os.path.exists(valid_output_path), "Valid image was not processed."
    assert not os.path.exists(invalid_output_path), "Invalid image should not be processed."

    
if __name__ == "__main__":
    pytest.main([__file__])

