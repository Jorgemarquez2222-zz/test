import logging
from django.core.files.uploadedfile import UploadedFile

from app_public.app.Configuration import FILE_HANDLER
from typing import Dict, Tuple


logger = logging.getLogger("django")
logger.setLevel(logging.INFO)
REQUEST_FILES_TYPE = Dict[str, UploadedFile]
IMAGE_SAVE_RESULT_TYPE = Tuple[bool, str]


def upload_photo(request_files: REQUEST_FILES_TYPE) -> IMAGE_SAVE_RESULT_TYPE:
    is_save_valid = True
    photo_id = ""
    if request_files is not None and len(request_files) > 0:
        logger.info("FILES is set")
        if len(request_files) == 1:
            for tag in request_files:
                photo = request_files[tag]
                photo_id = FILE_HANDLER.save(photo)
                logger.info("Photo id is %s" % photo_id)
        else:
            logger.error("Only one file should be uploaded")
            is_save_valid = False

    return is_save_valid, photo_id
