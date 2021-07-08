from flask import Blueprint, request

from be.configuration import CONFIGURATIONS
from be.persistency.persistence_api import persistence_api

user_data_api = Blueprint('user_data_api', __name__)


@user_data_api.route(CONFIGURATIONS['endpoints']['user_recent_tags'], methods=['POST', 'GET', 'OPTIONS'])
def interact_with_recent_tags():
    if request.method == 'POST':
        data = request.get_json()
        persistence_api.update_recent_tags(data)
        return {}
    if request.method == 'GET':
        tags = persistence_api.get_recent_tags()
        tags = tags.to_dict(orient='record')
        tags = tags[0]['last_search_tags']
        if(len(tags) < 1):
            response = [[], []]
        else:
            zipped = list(zip(tags[0], tags[1]))
            response = list(map(lambda e: {'tag_type': e[1], 'tag': e[0]}, zipped))

        return {'response': response}
    if request.method == 'OPTIONS':
        # preflight request
        return {}
