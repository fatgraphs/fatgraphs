from copy import deepcopy
from typing import List
from .model import User
from .interface import UserInterface
from .. import SessionLocal


class UserService:

    @staticmethod
    def get_by_name(userName: str, db) -> User:
        get = db.query(User).get(userName)
        return get

    @staticmethod
    def update_search_terms(user_name: str, metadata_object, db):
        user = UserService.get_by_name(user_name, db)
        recent_metadata_searches = deepcopy(user.recent_metadata_searches)
        if len(recent_metadata_searches) == 0:
            recent_metadata_searches = [[], []]

        recent_metadata_searches[0].insert(0, metadata_object["meta_value"])
        recent_metadata_searches[1].insert(0, metadata_object["meta_type"])
        recent_metadata_searches[0] = recent_metadata_searches[0][0:5]
        recent_metadata_searches[1] = recent_metadata_searches[1][0:5]

        user.recent_metadata_searches = recent_metadata_searches
        db.commit()
        return user