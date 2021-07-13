from flask import Blueprint, request

from be.configuration import CONFIGURATIONS
from be.persistency.persistence_api import persistenceApi

userDataApi = Blueprint('userDataApi', __name__)


@userDataApi.route(CONFIGURATIONS['endpoints']['userRecentMetadataSearches'], methods=['POST', 'GET', 'OPTIONS'])
def interactWithRecentMetadataSearches():
    if request.method == 'POST':
        body = request.get_json()
        persistenceApi.updateRecentMetadataSearches(body)
        return {}
    if request.method == 'GET':
        recentMetadataSearches = persistenceApi.getRecentMetadataSearches()
        recentMetadataSearches = recentMetadataSearches.to_dict(orient='record')
        recentMetadataSearches = recentMetadataSearches[0]['recent_metadata_searches']
        if len(recentMetadataSearches) < 1:
            response = [[], []]
        else:
            zipped = list(zip(recentMetadataSearches[0], recentMetadataSearches[1]))
            response = list(map(lambda e: {'metadata_value': e[0], 'metadata_type': e[1]}, zipped))

        return {'response': response}
    if request.method == 'OPTIONS':
        # preflight request
        return {}
