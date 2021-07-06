"""
Settings for Pyzantine. All configuration options go in this file.
"""
from pathlib import Path

# All image input and output folders
FILEPATHS = {
    "raw_source_image_library": Path("/Volumes/LaCie/Images/Main Library"),
    "output_folder_processed_sources": Path(
        "/Volumes/LaCie/Images/mosaic_source_images"
    ),
}

# Image sizing. Source images are square, measurement is px
SOURCE_IMAGE_WIDTH_HEIGHT = 50
