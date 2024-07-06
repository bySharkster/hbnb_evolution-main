from src import db
from src.models.base import Base
from src.persistence.repository import Repository
from utils.constants import USE_DATABASE_ENV_VAR

import os

class DBRepository(Repository):
    """A class representing a database repository."""

    def __init__(self) -> None:
        """
        Initialize the DBRepository.

        Sets the `use_database` attribute based on the value of the `USE_DATABASE` environment variable.
        """
        self.use_database = os.getenv(USE_DATABASE_ENV_VAR, 'False').lower() in ('true', '1', 't')

    def get_all(self, model_name: str) -> list:
        """
        Retrieve all objects of a given model from the database.

        Args:
            model_name (str): The name of the model.

        Returns:
            list: A list of objects of the specified model.

        Raises:
            ValueError: If the specified model name is invalid.
        """
        if self.use_database:
            model = self._get_model_by_name(model_name)
            if model_name:
                return db.session.query(model).all()
            else:
                raise ValueError(f"Invalid model name: {model_name}")
        else:
            # Implement file-based get_all logic
            pass

    def get(self, model_name: str, obj_id: str) -> Base | None:
        """
        Retrieve an object of a given model from the database.

        Args:
            model_name (str): The name of the model.
            obj_id (str): The ID of the object.

        Returns:
            Base | None: The object if found, None otherwise.

        Raises:
            ValueError: If the specified model name is invalid.
        """
        if self.use_database:
            model_name = globals().get(model_name)
            if model_name:
                return model_name.query.get(obj_id)
            else:
                raise ValueError(f"Invalid model name: {model_name}")
        else:
            # Implement file-based get logic
            pass

    def reload(self) -> None:
        """
        Reload the database session.

        Rolls back any pending changes in the session.

        Note:
            This method has no effect if `use_database` is False.
        """
        if self.use_database:
            db.session.rollback()
        else:
            # Implement file-based reload logic
            pass

    def save(self, obj: Base) -> None:
        """
        Save an object to the database.

        Args:
            obj (Base): The object to be saved.

        Note:
            This method has no effect if `use_database` is False.
        """
        if self.use_database:
            db.session.add(obj)
            db.session.commit()
        else:
            # Implement file-based save logic
            pass

    def update(self, obj: Base) -> Base | None:
        """
        Update an object in the database.

        Args:
            obj (Base): The object to be updated.

        Returns:
            Base | None: The updated object if successful, None otherwise.

        Note:
            This method has no effect if `use_database` is False.
        """
        if self.use_database:
            db.session.commit()
            return obj
        else:
            # Implement file-based update logic
            pass

    def delete(self, obj: Base) -> bool:
        """
        Delete an object from the database.

        Args:
            obj (Base): The object to be deleted.

        Returns:
            bool: True if the object was successfully deleted, False otherwise.

        Note:
            This method has no effect if `use_database` is False.
        """
        if self.use_database:
            db.session.delete(obj)
            db.session.commit()
            return True
        else:
            # Implement file-based delete logic
            pass
