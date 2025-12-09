import pytest

# Import your package modules
from nba_rebuilds import fetch_data, rebuilds, scraping

def test_imports():
    # Simple check that modules exist
    assert fetch_data is not None
    assert rebuilds is not None
    assert scraping is not None