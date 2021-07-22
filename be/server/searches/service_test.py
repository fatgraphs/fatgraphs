from typing import List

from be.server.searches import SearchTerm
from be.server.searches.service import SearchTermService
from .interface import SearchTermInterface
from ..test.fixtures import app, db

def test_get_recent_searches(db: object):  # noqa
    a: SearchTerm = SearchTerm(id=1, type="type", value="idex")
    b: SearchTerm = SearchTerm(id=2, type="label", value="test")
    c: SearchTerm = SearchTerm(id=3, type="type", value="dex")
    db.add(a)
    db.add(b)
    db.add(c)
    db.commit()

    results: List[SearchTerm] = SearchTermService.get_recent_searches(db)

    assert len(results) == 3
    assert a in results
    assert b in results
    assert c in results

def test_update_search_terms(db: object):  # noqa
    a: SearchTerm = SearchTerm(type="type", value="idex")
    b: SearchTerm = SearchTerm(type="label", value="test")
    c: SearchTerm = SearchTerm(type="type", value="dex")
    d: SearchTerm = SearchTerm(type="type", value="dex")
    e: SearchTerm = SearchTerm(type="type", value="dex")

    db.add(a)
    db.add(b)
    db.add(c)
    db.add(d)
    db.add(e)
    db.commit()

    update: SearchTermInterface = dict(type='blah', value='bar')

    results: List[SearchTerm] = SearchTermService.update_search_terms(update, db)

    assert len(results) == 5
    assert a not in results
    assert b in results
    assert c in results
    assert d in results
    assert e in results