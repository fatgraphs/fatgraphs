import io

import requests

from be.tile_creator_2.configs import settings
from be.utils import timeit


class ResourceApi():

    def __init__(self, url: str) -> None:
        self.url = settings.BASE_URL + url

    def get(self):
        
        response = requests.get(
            self.url, 
        )
        self.check_status_code(response)
        return response.json()

    def post(self, body: object):
        response = requests.post(self.url, json=body)
        self.check_status_code(response)
        return response.json()

    @timeit("Uploading took")
    def post_stream(self, df):
        csv_data = io.StringIO()

        df.to_csv(csv_data, index=False)

        response = requests.post(
            self.url, 
            data=csv_data.getvalue(), 
            stream=True
        )
    
        self.check_status_code(response)

        return response
    
    def check_status_code(self, response):
        if response.status_code >= 400:
            raise Exception(
                "Invalid status code in HTTP response", 
                f"Culprit URL is {self.url}"
            )


class GraphApi(ResourceApi):

    def __init__(self, url="") -> None:
        super().__init__("/graph/" + url)


class ConfigsApi(ResourceApi):

    def __init__(self, url="") -> None:
        super().__init__("/graph_configuration/" + url)


class VertexApi(ResourceApi):

    def __init__(self, url="") -> None:
        super().__init__("/vertex" + url)


class VerticesApi(VertexApi):

    def __init__(self, url="") -> None:
        super().__init__("/upload" + url)

class VertexMetadataApi(ResourceApi):

    def __init__(self) -> None:
        super().__init__("/vertex-metadata")

    def get_all_for_graph(self, graph_id):
        '''Givenn graph_id returns all the metadata associated with the
        vertices in this graph'''
        response = requests.get(
            self.url + f"/{graph_id}", 
            stream=True
        )
        self.check_status_code(response)
        return response
    
class EdgesApi(ResourceApi):
    def __init__(self) -> None:
        super().__init__("/edge/upload")

class GraphCategory(ResourceApi):
    def __init__(self):
        super().__init__("/gallery_categories")

class TileApi(ResourceApi):
    def __init__(self):
        super().__init__("/tile")

    def post_tile(self, img_data, z, x, y, graph_id):
        response = requests.post(
            self.url + f"/{graph_id}/{z}/{x}/{y}.png",
            files={"image": img_data}
        )
        self.check_status_code(response)
        return response
    
    def post_plot(self, img_data, z, graph_id):
        response = requests.post(
            self.url + f"/plot/{graph_id}/{z}",
            files={"image": img_data}
        )
        self.check_status_code(response)
        return response
    

class ApiLayer():

    graph = GraphApi()
    gallery_category = GraphCategory()
    configs = ConfigsApi()
    vertex = VertexApi()
    vertices = VerticesApi()
    vertex_metadata = VertexMetadataApi()
    edges = EdgesApi()
    tile = TileApi()