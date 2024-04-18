"""Create a unique storage instance for your application"""

from os import environ
from property_models.engine.file_storage import FileStorage
from property_models.base_model import BaseModel
from property_models.user import User
from property_models.state import State
from property_models.city import City
from property_models.amenity import Amenity
from property_models.place import Place
from property_models.review import Review

storage_type = "PROPERTY_STORAGE_TYPE"
if storage_type in environ.keys() and environ["PROPERTY_STORAGE_TYPE"] == "db":
    storage = PropertyStorage()
    storage.reload()
else:
    storage = FileStorage()
    storage.reload()
