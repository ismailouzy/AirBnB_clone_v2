#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from os import getenv
from models.base_model import Base

class DBStorage:
    ''' Handles database engine '''
    __engine = None
    __session = None

    def __init__(self):
        ''' Create engine for database '''
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        ''' query for all objects on the current database session '''
        from models import base_model

        classes = {'BaseModel': base_model.BaseModel}
        if cls:
            classes.update({'User': base_model.User, 'State': base_model.State,
                            'City': base_model.City, 'Amenity': base_model.Amenity,
                            'Place': base_model.Place, 'Review': base_model.Review})

        result = {}
        if cls:
            if isinstance(cls, str):
                cls = classes.get(cls, None)
            if cls:
                try:
                    query_rows = self.__session.query(cls).all()
                    for obj in query_rows:
                        key = '{}.{}'.format(type(obj).__name__, obj.id)
                        result[key] = obj
                except SQLAlchemyError as e:
                    # Handle database errors
                    print(f"An error occurred: {e}")
        else:
            for name, value in classes.items():
                try:
                    query_rows = self.__session.query(value).all()
                    for obj in query_rows:
                        key = '{}.{}'.format(name, obj.id)
                        result[key] = obj
                except SQLAlchemyError as e:
                    # Handle database errors
                    print(f"An error occurred: {e}")
        return result

    def new(self, obj):
        ''' add the object to the current database session '''
        try:
            self.__session.add(obj)
        except SQLAlchemyError as e:
            # Handle database errors
            print(f"An error occurred: {e}")

    def save(self):
        ''' commit all changes of the current database session '''
        try:
            self.__session.commit()
        except SQLAlchemyError as e:
            # Handle database errors
            print(f"An error occurred: {e}")

    def delete(self, obj=None):
        ''' delete obj from the current database session '''
        if obj:
            try:
                self.__session.delete(obj)
            except SQLAlchemyError as e:
                # Handle database errors
                print(f"An error occurred: {e}")

    def reload(self):
        ''' create all tables in the database '''
        try:
            Base.metadata.create_all(self.__engine)
            session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
            Session = scoped_session(session_factory)
            self.__session = Session()
        except SQLAlchemyError as e:
            # Handle database errors
            print(f"An error occurred: {e}")

    def close(self):
        ''' close the session '''
        try:
            self.__session.close()
        except SQLAlchemyError as e:
            # Handle database errors
            print(f"An error occurred: {e}")
