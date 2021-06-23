from flask import Blueprint, request

from be.configuration import CONFIGURATIONS
from be.persistency.nice_abstraction import singletonNiceAbstraction

user_data_api = Blueprint('user_data_api', __name__)


@user_data_api.route(CONFIGURATIONS['endpoints']['user_recent_tags'], methods=['POST', 'GET', 'OPTIONS'])
def interact_with_recent_tags():
    if request.method == 'POST':
        data = request.get_json()
        singletonNiceAbstraction.update_recent_tags(data)
        return {}
    if request.method == 'GET':
        tags = singletonNiceAbstraction.get_recent_tags()
        response = tags.to_dict(orient='record')
        tags = response[0]['last_search_tags'].split(' ')
        return {'response': tags}
    if request.method == 'OPTIONS':
        # preflight request
        return {}