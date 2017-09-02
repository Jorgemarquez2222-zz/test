import uuid

from django.core.files.uploadedfile import UploadedFile
from abc import ABCMeta, abstractmethod


class FileHandler(metaclass=ABCMeta):

    @abstractmethod
    def save(self, file: UploadedFile) -> str:
        pass

    @abstractmethod
    def load(self, file_id: str) -> bytes:
        pass

    @abstractmethod
    def delete(self, file_id: str):
        pass

    @abstractmethod
    def get_url(self, file_id : str) -> str:
        pass

    @classmethod
    def generate_random_id(cls):
        return uuid.uuid4()
