from app import db
from typing import List
from .model import User
from .interface import UserInterface


class UserService:
    # @staticmethod
    # def get_all() -> List[Graph]:
    #     return Graph.query.all()

    @staticmethod
    def get_by_name(userName: str) -> User:
        get = User.query.get(userName)
        return get

    @staticmethod
    def update_search_terms(user_name: str, search_term):
        user = UserService.get_by_name(user_name)
        recent_metadata_searches = [e for e in user.recent_metadata_searches] # getattr(self, "recent_metadata_searches")
        recent_metadata_searches.insert(0, search_term)
        recent_metadata_searches = recent_metadata_searches[0:5]
        user.recent_metadata_searches = recent_metadata_searches  # setattr(self, "recent_metadata_searches", recent_metadata_searches[0:5]
        db.session.commit()
        return user


# @staticmethod
# def update(widget: Graph, Widget_change_updates: GraphInterface) -> Graph:
#     widget.update(Widget_change_updates)
#     db.session.commit()
#     return widget

# @staticmethod
# def delete_by_id(widget_id: int) -> List[int]:
#     widget = Graph.query.filter(Graph.graph_id == widget_id).first()
#     if not widget:
#         return []
#     db.session.delete(widget)
#     db.session.commit()
#     return [widget_id]
#
# @staticmethod
# def create(new_attrs: GraphInterface) -> Graph:
#     new_widget = Graph(name=new_attrs["name"], purpose=new_attrs["purpose"])
#
#     db.session.add(new_widget)
#     db.session.commit()
#
#     return new_widget
