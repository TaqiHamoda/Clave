from __future__ import annotations

from models.base import Base

import base64
import os


class Image(Base):
    _CLASS: str = "image"
    _properties: dict[str, object] = {
        "name": str,
        "image": str
    }

    name: str = None
    image: str = None

    def toDict(self) -> dict:
        return {
            "name": self.name,
            "image": self.image,
        }

    @classmethod
    def fromDict(cls: Image, data: dict) -> Image | None:
        if not cls.isValid(data):
            return None

        model: Image = Image(data["name"], cls._CLASS)

        model.name = cls._properties["name"](data["name"])
        model.image = cls._properties["image"](data["image"])

        return model


    @classmethod
    def fromFile(cls: Image, file_path: str) -> Image | None:
        image: bytes = None
        
        with open(file_path, "rb") as f:
            image = base64.b64encode(f.read())

        return cls.fromDict({
            "name": os.path.basename(file_path),
            "image": image.decode("utf-8")
        })
        

