"""
Create a mosaic image from a target image and source images.
The sequence is:
1. Load a target image. This is the "big picture" which will be made up of smaller source images.
2. Divide the target image into squares with an edge of n pixels where n is the edge-length of the source images.
3. Iterate over these squares, calculating the average RGB value, selecting the source image with the closest RGB value
and pasting that source image into the target image square.
"""

import math, json, time
from pathlib import Path
from PIL import Image
import settings
from settings import FILEPATHS


def calculate_euclidean_distance(square, source_image):
    """
    Calculate the difference in average RGB values between two images.
    See https://en.wikipedia.org/wiki/Color_difference#sRGB
    """
    per_channel_differences = []
    for channel in zip(square, source_image):
        channel_difference = int(channel[1]) - int(channel[0])
        per_channel_differences.append(channel_difference ** 2)

    return sum(per_channel_differences) ** 0.5


def find_nearest_euclidean_distance(square):
    """
    Work through the images listed in source_images.json. Return the path to the source image
    with the smallest Euclidean distance to the supplied square of the input image
    """
    with open(FILEPATHS["source_images_data"]) as fin:
        source_images = json.loads(fin.read())

    nearest_match = None
    for file, average_colour in source_images.items():

        if file == "meta":  # ignore the metadata section of the file
            continue

        if not nearest_match:  # First iteration
            closest_distance = calculate_euclidean_distance(square, average_colour)
            nearest_match = file
        else:
            distance = calculate_euclidean_distance(square, average_colour)
            if distance < closest_distance:
                closest_distance = distance
                nearest_match = file
    return nearest_match


def move_right(window, edge):
    new_window = [
        window[0] + edge,
        window[1],
        window[2] + edge,
        window[3],
    ]
    return new_window


def move_to_start_of_next_row(window, edge):
    new_window = [
        0,
        window[1] + edge,
        edge,
        window[3] + edge,
    ]
    return new_window


def calculate_average_colour(region):
    pixels = region.getdata()
    red = int(sum([x[0] for x in pixels]) / len(pixels))
    green = int(sum([x[1] for x in pixels]) / len(pixels))
    blue = int(sum([x[2] for x in pixels]) / len(pixels))

    return (red, green, blue)


def calculate_number_of_source_images(width, height):
    return (
        int(math.ceil(width / settings.SOURCE_IMAGE_WIDTH_HEIGHT)),
        int(math.ceil(height / settings.SOURCE_IMAGE_WIDTH_HEIGHT)),
    )


def main():
    start = time.perf_counter()
    # Create top layer i.e. the picture that we will paste onto the base layer
    window = (
        0,
        0,
        settings.SOURCE_IMAGE_WIDTH_HEIGHT,
        settings.SOURCE_IMAGE_WIDTH_HEIGHT,
    )

    input_img = Image.open(FILEPATHS["test_image"])

    # Calculate how many source images we need to cover the input image
    input_img_width = input_img.size[0]
    input_img_height = input_img.size[1]
    source_images_width, source_images_height = calculate_number_of_source_images(
        input_img_width, input_img_height
    )

    # Uncomment the line below if the image needs to be rotated
    # input_img = input_img.transpose(Image.ROTATE_90)

    qty_analysed = 1
    for i in range(source_images_height):  #
        for j in range(source_images_width):
            # calculate average colour of square
            average_colour = calculate_average_colour(input_img.crop(window))

            # get source image with closest match
            closest_image: str = find_nearest_euclidean_distance(average_colour)

            # paste source image over square
            this_source_image = Image.open(Path(closest_image))
            crop_area = (
                0,
                0,
                settings.SOURCE_IMAGE_WIDTH_HEIGHT,
                settings.SOURCE_IMAGE_WIDTH_HEIGHT,
            )
            paste_region = this_source_image.crop(crop_area)

            input_img.paste(paste_region, window)
            window = move_right(window, settings.SOURCE_IMAGE_WIDTH_HEIGHT)
            print(f"analysed {qty_analysed} squares")
            qty_analysed += 1
        window = move_to_start_of_next_row(window, settings.SOURCE_IMAGE_WIDTH_HEIGHT)

    end = time.perf_counter()
    elapsed = end - start
    print(f"finished in {elapsed} seconds")
    input_img.show()


if __name__ == "__main__":
    main()
