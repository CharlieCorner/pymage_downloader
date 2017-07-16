from abc import abstractmethod


class BaseParser():
    @abstractmethod
    def get_images(self, post):
        raise NotImplementedError("A concrete parser must be used")
