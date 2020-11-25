"""Sisältää yksikkötestit luokalle ReportReader."""
import pytest

from ..model.report_reader import ReportReader

START_DATE = "2020-12-24"
END_DATE = "2021-1-24"
SAVE_DIR = "./resources"

@pytest.fixture()
def handler():
    """Returns a ReportReader instantiated with test parameters."""
    return ReportReader(START_DATE, END_DATE, SAVE_DIR)

def test_read_from_date(handler):
    expected = {
        "afds": 3,
        "Käteisnostot": 16,
        "Tulot yht.": 4,
        "Muut tulot": -21,
        "Menot yht.": 31,
        "Muut menot": -16,
        "Tase": 18
        }
    actual = handler.read()
    assert expected == actual
