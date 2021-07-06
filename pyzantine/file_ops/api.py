"""
Functions related to file handling.
"""
import os
from pathlib import Path
from PIL import Image, UnidentifiedImageError


def find_jpgs_in_tree(start: Path) -> Path:
    """
    Walks through a directory tree, yielding any jpeg files found.
    """
    for root, dirs, files in os.walk(start):
        for file in files:
            if file.split(".")[-1].lower() in ["jpg", "jpeg"]:
                path = Path(root) / file
                yield path.absolute()


def write_file(image: Image.Image, output_path: Path):
    """
    Saves a jpg image to disk.
    """
    image.save(output_path)


def read_file(image_path: Path) -> Image.Image:
    """
    Reads a jpg image from disk.
    """
    try:
        source_image = Image.open(image_path)
    except UnidentifiedImageError:
        raise UnidentifiedImageError

    return source_image
