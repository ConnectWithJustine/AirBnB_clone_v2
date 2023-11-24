#!/usr/bin/python3
"""
Contains the class DBstorage
"""

from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}

class DBStorage:
    """ Interacts with the MySQL DB"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage obj"""
        HBNB_MYSQL_USER = getenv("HBNB_MYSQL_USER")
        HBNB_MYSQL_PWD = getenv("HBNB_MYSQL_PWD")
        HBNB_MYSQL_HOST = getenv("HBNB_MYSQL_HOST")
        HBNB_MYSQL_DB = getenv("HBNB_MYSQL_DB")
        HBNB_ENV = getenv("HBNB_ENV")
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadat.drop_all(self.__engine)

        def all(self, cls=None):
            """query on the current database session"""
            temp = {}
            for cl in classes:
            if cls is None or cls is classes[cl] or cls is cl:
                objs = self.__session.query(classes[cl]).all()
                for obj in objs:
                    key = oobj.__class__.__name__+ '.' + obj.id
                    temp[key] = obj
            return (temp)

        def new(self, obj):
            """Add the objec to the current datbase session"""
            self.__session.add(obj)

        def save(self):
            """Commit all changes of the current database session"""
            self.__session.commit()

        def delete(self, obj=None):
            """Delet from the current database session obj if not None"""
            if obj is not None:
                self.__session.delete(obj)

        def reload(self):
            """reloads data from the database"""
            Base.metadata.create_all(self.__engine)
            sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
            session = scoped_session(sess_factory)
            self.__session = Session

        def close(self):
            """call remove() method on the private session attribute"""
            self.__session.remove()
