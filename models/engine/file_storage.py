#!/usr/bin/python3
"""Handles storage of instances for the AirBnB project"""

import json
import sys
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """Serializes instances to a JSON file and deserializes JSON file to instances

    Attributes:
        __file_path: Path to the JSON file
        __objects: Objects will be stored
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of stored objects

        Args:
            cls: Class name to filter objects

        Returns:
            A dictionary of filtered or all objects
        """
        if cls is None:
            return self.__objects
        else:
            filtered_dict = {}
            if len(self.__objects) > 0:
                for key, value in self.__objects.items():
                    if isinstance(cls, str):
                        if cls == key.split('.')[0]:
                            filtered_dict[key] = value
                    else:
                        if isinstance(value, cls):
                            filtered_dict[key] = value
            return filtered_dict

    def new(self, obj):
        """Adds a new object to storage

        Args:
            obj: The object to add
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """Serializes objects to JSON file"""
        serialized_objs = {}
        for key, value in self.__objects.items():
            serialized_objs[key] = value.to_dict()
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(serialized_objs, f)

    def reload(self):
        """Deserializes JSON file to objects"""
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                for key, value in json.load(f).items():
                    value = eval(value["__class__"])(**value)
                    self.__objects[key] = value
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes an object from storage

        Args:
            obj: The object to delete
        """
        obj_key = ""
        for key, value in self.__objects.items():
            if obj == value:
                obj_key = key
        if obj_key != "":
            del self.__objects[obj_key]

    def close(self):
        """Closes the storage"""
        self.reload()
