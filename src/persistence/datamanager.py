from pyexpat import model
from flask import app
from sqlalchemy import delete
from src import db
from src.persistence.file import FileRepository as file_manager
from src.persistence.db import DBRepository as db_manager
from src.models.base import Base
from utils.constants import USE_DATABASE_ENV_VAR
import os

# Data Manager for the persistence layer
class DataManager:
   
   def __init__(self) -> None:
     """Initialize the DataManager class.:
         Sets the `use_database` attribute based on the value of the `USE_DATABASE` environment variable.
     """
     self.use_database = os.getenv(USE_DATABASE_ENV_VAR, 'False').lower() in ('true', '1', 't')

   def save(self, obj: Base):
     if self.use_database:
       db_manager.save(self, obj)
     else:
       file_manager.save(self, obj)
   
   def get(self, model_name: str, obj_id: str):
     if self.use_database:
       db_manager.get(self, model_name, obj_id)
     else:
       file_manager.get(self, model_name, obj_id)
     
   def get_all(self, model_name: str):
     if self.use_database:
       db_manager.get_all(self, model_name)
     else:
       file_manager.save(self, model_name)
     
   def update(self, obj: Base):
     if self.use_database:
       db_manager.update(self, obj)
     else:
       file_manager.update(self, obj)
     
   def delete(self, obj: Base):
     if self.use_database:
       db_manager.delete(self, obj)
     else:
       file_manager.delete(self, obj)
