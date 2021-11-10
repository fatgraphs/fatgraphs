from typing import List
from . import Graph
from .service import GraphService
from ..test.fixtures import app, db

def test_get_all(db: object):  # noqa
    a: Graph = Graph(graph_name='bello')
    b: Graph = Graph(graph_name='bello3')
    c: Graph = Graph(graph_name='bello2')

    db.add(a)
    db.add(b)
    db.add(c)
    db.commit()

    results: List[Graph] = GraphService.get_all(db)

    assert len(results) == 3
    assert a in results
    assert b in results
    assert c in results
