import json
import requests

from be.tile_creator_2.configs import settings


class ResourceApi():

    def __init__(self, url: str) -> None:
        self.url = settings.BASE_URL + url

    def post(self, body: object):
        response = requests.post(self.url, json=body)
        print(response.text)
        return response.json()


class GraphApi(ResourceApi):

    def __init__(self, url="") -> None:
        super().__init__("/graph/" + url)


class ConfigsApi(ResourceApi):

    def __init__(self, url="") -> None:
        super().__init__("/graph_configuration/" + url)


class ApiLayer():

    graph = GraphApi()
    configs = ConfigsApi()