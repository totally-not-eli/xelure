from sqlalchemy import create_engine, select, inspect, and_, or_, not_
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.orm.attributes import instance_dict

import pandas as pd

from models import *


class DynamicModelMeta(Base.__class__):
    def __new__(cls, name, bases, attrs):
        # Add additional attributes or methods to the dynamic model
        attrs['additional_attribute'] = 'This is an additional attribute'

        # Create a new class inheriting from existing models
        new_class = super().__new__(cls, name + 'Dynamic', bases, attrs)

        return new_class
    
class HelperCSV:
    def __init__(self, csv_file_path, model_class, session, mapper={}):
        self.csv_file_path : str = csv_file_path
        self.model = model_class
        self.session : Session = session
        self.mapper = mapper
        
    def create_dynamic_model(self):
        class DynamicModel(self.model, metaclass=DynamicModelMeta):
            pass
        return DynamicModel
    
    def read_csv(self) -> list:
        """If class is initialized with a file path, 

        Returns:
            list: returns list of dict with proper fields
        """
        if self.mapper:
            return pd.read_excel(self.csv_file_path).fillna("").rename(columns=self.mapper).to_dict(orient="records")
        return pd.read_excel(self.csv_file_path).fillna("").to_dict(orient="records")

    def seed_data_from_csv(self, rows =[]) -> bool:
        try:
            batch_size = 100  # Set the desired batch size
            
            if not rows:
                rows = self.read_csv()
                
            for i in range(0, len(rows), batch_size):
                batch_rows = rows[i:i + batch_size]

                dynamic_models = [self.create_dynamic_model()(**row) for row in batch_rows]
                self.session.add_all(dynamic_models)
                self.session.commit()
                self.session.flush()  # Optional: flush the session to clear the session's state and release resources
                
        except Exception as e:
            print("Error")
            print(e)