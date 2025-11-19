#!/usr/bin/env python3

"""
Authored by: Potjamarn Arpornratn
Date: Nov 19, 2025

This script will scale and convert images in a given folder.
Usage: python image_scaling.py
"""

import os
from PIL import Image

def process_images(input_folder, output_folder):
    """Rotate, resize, and convert images in the input folder and save to output folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        img_path = os.path.join(input_folder, filename)
        try:
            with Image.open(img_path) as img:
                # print(f"Processing: {img_path}")
                # Rotate 90 degrees clockwise
                img = img.rotate(-90)
                # Resize to 128x128
                img = img.resize((128, 128))
                # Save as JPEG in output folder
                base_filename = os.path.splitext(filename)[0]
                output_path = os.path.join(output_folder, f"{base_filename}.jpeg")
                print(output_path)
                # img = img.convert('RGB')
                img.convert('RGB').save(output_path, 'JPEG')
                # print(f"Processed and saved: {output_path}")
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
                

if __name__ == "__main__":
    input_folder = "./images/"  # Folder containing original images
    output_folder = "./opt/icons/"  # Folder to save processed images
    process_images(input_folder, output_folder)