import logging
import os

from django.core.files.uploadedfile import UploadedFile

from app_public.app.FileHandler import FileHandler

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)


class LocalFileHandler(FileHandler):
    URL_STATIC = "/static/photos/%s"
    PUBLIC_STATIC_S = "./app_public%s" % URL_STATIC

    def get_url(self, file_id : str) -> str:
        return LocalFileHandler.URL_STATIC % file_id

    @classmethod
    def generate_file_name(cls, file_id: str) -> str:
        return LocalFileHandler.PUBLIC_STATIC_S % file_id

    def save(self, file: UploadedFile) -> str:
        logger.info("Reading file of type %s and size %d" % (file.content_type, file.size))
        file_id = super(LocalFileHandler, self).generate_random_id()
        file_name = LocalFileHandler.generate_file_name(file_id)
        # create directory if it doesn't exist yet
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with open(file_name, "wb+") as photo_file:
            photo_file.write(file.read())
        return file_id

    def load(self, file_id: str) -> bytes:
        with open(LocalFileHandler.generate_file_name(file_id), "rb") as file:
            return file.read()

    def delete(self, file_id: str):
        os.remove(LocalFileHandler.generate_file_name(file_id))
