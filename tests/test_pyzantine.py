from pathlib import Path
from PIL import Image, UnidentifiedImageError
from pytest import raises
from pyzantine import __version__
from pyzantine.file_ops import read_file, find_jpgs_in_tree
from pyzantine.source_imgs.process import crop_to_square, resize


def test_version():
    assert __version__ == "0.1.0"


def test_read_file():
    test_img = "/Users/rich/code/pyzantine/tests/test_data/good_test_data/test_img.JPG"
    image_path = Path(test_img)
    img = read_file(image_path)
    assert isinstance(img, Image.Image)


def test_find_jpgs_in_tree_good():
    """
    Test that find_jpgs_in_tree() returns the correct response when there is valid data in the
    target folder
    """
    test_path = Path("/Users/rich/code/pyzantine/tests/test_data/good_test_data")
    jpgs = [img for img in find_jpgs_in_tree(test_path)]
    print(jpgs)
    assert jpgs == [
        Path("/Users/rich/code/pyzantine/tests/test_data/good_test_data/test_img2.JPG"),
        Path("/Users/rich/code/pyzantine/tests/test_data/good_test_data/test_img.JPG"),
    ]


def test_find_jogs_in_tree_bad():
    """
    Test that find_jpgs_in_tree() raises the correct error when it can't load an image
    """
    test_path = Path("/Users/rich/code/pyzantine/tests/test_data/bad_test_data")
    jpgs = (img for img in find_jpgs_in_tree(test_path))
    with raises(UnidentifiedImageError):
        for file in jpgs:
            read_file(file)


def test_crop_to_square():
    """
    Test that crop_to_square() returns a square image when given a rectangular one
    """
    test_img = "/Users/rich/code/pyzantine/tests/test_data/good_test_data/test_img.JPG"
    image_path = Path(test_img)
    img = read_file(image_path)
    short_edge = min(img.size)
    cropped = crop_to_square(img)
    for i in cropped.size:
        assert i == short_edge


def test_resize():
    """
    Test that resize() correctly resizes a square image.
    """
    from settings import SOURCE_IMAGE_WIDTH_HEIGHT

    test_img = "/Users/rich/code/pyzantine/tests/test_data/good_test_data/test_img.JPG"
    image_path = Path(test_img)
    img = read_file(image_path)

    # Prove that the starting image is larger than the resized image will be
    for i in img.size:
        assert i > SOURCE_IMAGE_WIDTH_HEIGHT

    resized = resize(img)
    for i in resized.size:
        assert i == SOURCE_IMAGE_WIDTH_HEIGHT
