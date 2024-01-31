from sqlalchemy import create_engine, select, inspect, and_, or_, not_
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.orm.attributes import instance_dict

import inspect
import importlib
import json
import re
import os 

from models import *
from utils.general_utils import *

class DynamicModelMeta(Base.__class__):
    def __new__(cls, name, bases, attrs):
        # Add additional attributes or methods to the dynamic model
        attrs['additional_attribute'] = 'This is an additional attribute'

        # Create a new class inheriting from existing models
        new_class = super().__new__(cls, name + 'Dynamic', bases, attrs)

        return new_class

class SQLUtils(GeneralUtils):
    @staticmethod
    def queryset_to_json(queryset):
        return json.dumps([dict(row) for row in queryset.all()], indent=2)
        
    @staticmethod
    def get_model_attributes(model_instance):
        """
        Get all key-value pairs of a SQLAlchemy model instance.
        
        Args:
            model_instance: An instance of the SQLAlchemy model.

        Returns:
            dict: A dictionary containing key-value pairs of the model attributes.
        """
        
        from sqlalchemy import inspect
        
        inspector = inspect(model_instance)
        attributes = inspector.attrs

        return {attr.key: attr.value for attr in attributes}

    @staticmethod
    def extract_table_names():
        table_names = []

        # Use locals() to get the current module's namespace
        current_module = importlib.import_module(__name__)
        
        for name in dir(current_module):
            obj = getattr(current_module, name)
            if hasattr(obj, '__tablename__'):
                table_names.append(getattr(obj, '__tablename__'))

        return table_names
    
    @staticmethod
    def get_model_class(table_name):
        # Use locals() to get the current module's namespace
        current_module = importlib.import_module(__name__)

        for name in dir(current_module):
            obj = getattr(current_module, name)
            if inspect.isclass(obj) and hasattr(obj, '__tablename__') and getattr(obj, '__tablename__') == table_name:
                return obj

        return None
    
    @staticmethod
    def get_all_model_classes():
        """Get all model classes from the current module."""
        current_module = importlib.import_module(__name__)
        return [obj for name, obj in inspect.getmembers(current_module) if inspect.isclass(obj) and hasattr(obj, '__table__')]

class Database(SQLUtils):
    def __init__(self, db_endpoint="local_database.db", dialect="sqlite"):
        self.db_url = f'{dialect}:///{db_endpoint}'
        self.engine = create_engine(self.db_url)
        self.batch_add = []
        
    def query_table(self, model_class, filters: dict = {}):
    
        """ query table after retrievings its table name / helper only. """
        
        try:
            with Session(self.engine) as session:
                query = session.query(model_class)

                # Apply filters if provided
                if filters:
                    filter_conditions = [getattr(model_class, key) == value for key, value in filters.items()]
                    query = query.filter(and_(*filter_conditions))

                # Execute the query and fetch the results
                results = query.all()

                # Convert results to a list of dictionaries with primitive attributes
                results = [self.get_model_attributes(row) for row in results]
                results = [self.filter_primitive_attributes(row) for row in results]

                return results
        
        except Exception as e:
            traceback.print_exc()
            
        finally:
            session.close()
            