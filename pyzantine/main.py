from settings import FILEPATHS, SOURCE_IMAGE_WIDTH_HEIGHT

fp = FILEPATHS["raw_source_image_library"]
edge_px = SOURCE_IMAGE_WIDTH_HEIGHT
from pyzantine.file_ops import find_jpgs_in_tree
from pathlib import Path

for i in (
    x
    for x in find_jpgs_in_tree(
        Path("/Users/rich/code/pyzantine_poc/tests/fixtures/test_images_lvl_1")
    )
):
    print(i)

from tests.test_pyzantine import test_find_jpgs_in_tree_good

test_find_jpgs_in_tree_good()
