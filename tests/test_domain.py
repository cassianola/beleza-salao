from datetime import time
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
import pytest

# Load the pure business rules without requiring Flask or a database.
spec = spec_from_file_location('domain', Path(__file__).parents[1] / 'app' / 'domain.py')
domain = module_from_spec(spec)
spec.loader.exec_module(domain)

@pytest.mark.parametrize('a,da,b,db,expected', [
    (time(10),60,time(10,30),45,True),
    (time(10),60,time(11),45,False),
    (time(10),60,time(9,30),60,True),
    (time(10),60,time(9),60,False),
    (time(10),60,time(10),60,True),
])
def test_overlap(a, da, b, db, expected):
    assert domain.overlap(a, da, b, db) is expected

@pytest.mark.parametrize('start,duration,expected', [
    (time(9),60,True), (time(17),60,True), (time(17,30),60,False),
    (time(8,30),60,False), (time(9),0,False),
])
def test_opening_hours(start, duration, expected):
    assert domain.within_hours(start, duration, time(9), time(18)) is expected

def test_invalid_date():
    with pytest.raises(ValueError):
        domain.parse_date('2026-02-30')

def test_invalid_time():
    with pytest.raises(ValueError):
        domain.parse_time('25:00')
