from PIL import Image
from settings import SOURCE_IMAGE_WIDTH_HEIGHT as EDGE


def crop_to_square(source_image: Image) -> Image:
    """
    Crop a square region of an image with sides equal to the shortest edge of the source
    image.
    """
    short_edge_length_px = min(source_image.size)
    crop = source_image.crop((0, 0, short_edge_length_px, short_edge_length_px))
    cropped_image = Image.new("RGB", (short_edge_length_px, short_edge_length_px))
    cropped_image.paste(crop)

    return cropped_image


def resize(square_image: Image) -> Image.Image:
    """
    Resize an already-square image. Uses the SOURCE_IMAGE_WIDTH_HEIGHT constant from
    settings.py as the length of the image's edges.
    """
    return square_image.resize((EDGE, EDGE))
