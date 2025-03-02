import os
import shutil
import tempfile

from django.conf import settings
from django.core.files.storage import default_storage as storage
from django.test.utils import override_settings

import pytest

from PIL import Image

from olympia.amo.tests.test_helpers import get_image_path
from olympia.users.tasks import delete_photo, resize_photo


pytestmark = pytest.mark.django_db


def test_delete_photo():
    with tempfile.TemporaryDirectory(dir=settings.TMP_PATH) as tmp_media_path:
        os.mkdir(os.path.join(tmp_media_path, 'userpics'))
        dst_path = os.path.join(tmp_media_path, 'userpics', 'foo.png')
        with storage.open(dst_path, mode='wb') as dst:
            dst.write(b'test data\n')
        with override_settings(MEDIA_ROOT=tmp_media_path):
            delete_photo(dst_path)

        assert not storage.exists(dst_path)


def test_resize_photo():
    somepic = get_image_path('sunbird-small.png')

    src = tempfile.NamedTemporaryFile(
        mode='r+b', suffix='.png', delete=False, dir=settings.TMP_PATH
    )
    dest = tempfile.NamedTemporaryFile(mode='r+b', suffix='.png', dir=settings.TMP_PATH)

    shutil.copyfile(somepic, src.name)

    src_image = Image.open(src.name)
    assert src_image.size == (64, 64)
    resize_photo(src.name, dest.name)

    # Image is smaller than 200x200 so it should stay the same.
    dest_image = Image.open(dest.name)
    assert dest_image.size == (64, 64)


def test_resize_photo_poorly():
    """If we attempt to set the src/dst, we do nothing."""
    somepic = get_image_path('mozilla.png')
    src = tempfile.NamedTemporaryFile(
        mode='r+b', suffix='.png', delete=False, dir=settings.TMP_PATH
    )
    shutil.copyfile(somepic, src.name)
    src_image = Image.open(src.name)
    assert src_image.size == (339, 128)

    resize_photo(src.name, src.name)

    # assert nothing happened
    src_image = Image.open(src.name)
    assert src_image.size == (339, 128)
