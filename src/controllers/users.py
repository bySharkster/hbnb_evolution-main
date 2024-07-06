"""
Users controller module
"""

from flask import abort, request
from src.models.user import User
from src.persistence.datamanager import DataManager as data_manager


def get_users():
    """Returns all users"""
    users: list[User] = User.get_all()

    return [user.to_dict() for user in users]


def create_user():
    """Creates a new user"""
    data = request.get_json()

    try:
        user = User.create(data)
        data_manager.save(user)
        
    except KeyError as e:
        abort(400, f"Missing field: {e}")
        
    except ValueError as e:
        abort(400, str(e))

    if user is None:
        abort(400, "User already exists")

    return user.to_dict(), 201


def get_user_by_id(user_id: str):
    """Returns a user by ID"""
    try:
        user = User.get(user_id)
        data_manager.get(User, user_id)
    except ValueError as e:
        abort(400, str(e))

    if not user:
        abort(404, f"User with ID {user_id} not found")

    return user.to_dict(), 200


def update_user(user_id: str):
    """Updates a user by ID"""
    data = request.get_json()

    try:
        user = User.update(user_id, data)
        data_manager.update(user)
    except ValueError as e:
        abort(400, str(e))

    if user is None:
        abort(404, f"User with ID {user_id} not found")

    return user.to_dict(), 200


def delete_user(user_id: str):
    """Deletes a user by ID"""

    try :
        user = User.get(user_id)
        data_manager.delete(user)
    except ValueError as e:
        abort(400, str(e))

    if not User.delete(user_id):
        abort(404, f"User with ID {user_id} not found")


    return "", 204

