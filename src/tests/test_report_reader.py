"""Sisältää yksikkötestit luokalle ReportReader."""
import datetime
from decimal import Decimal

import pytest

from ..model.report_reader import ReportReader

START_DATE = "2020-12-24"
END_DATE = "2021-2-24"
SAVE_DIR = "./resources"

@pytest.fixture()
def handler():
    """Returns a ReportReader instantiated with test parameters."""
    return ReportReader(SAVE_DIR)

def test_read_from_date_to_current_month(handler):
    dict1 = {
            'afds': Decimal('-3'),
            'Käteisnostot': Decimal('3'),
            'Tulot yht.': Decimal('-2'),
            'Muut tulot': Decimal('4'),
            'Menot yht.': Decimal('3'),
            'Muut menot': Decimal('2'),
            'Tase': Decimal('2'),
            'timestamp': datetime.date(2021, 3, 24)
        }

    dict2 = {
            'afds': Decimal('2'),
            'Käteisnostot': Decimal('7'),
            'Tulot yht.': Decimal ('9'),
            'Muut tulot': Decimal('-20'),
            'Menot yht.': Decimal('6'),
            'Muut menot': Decimal('-1'), 'Tase': Decimal('6'),
            'timestamp': datetime.date(2021, 2, 24)
        }

    dict3 = {
            'afds': Decimal('3'),
            'Käteisnostot': Decimal ('-1'),
            'Tulot yht.': Decimal('3'),
            'Muut tulot': Decimal('-6'),
            'Menot yht.': Decimal('14'),
            'Muut menot': Decimal('-8'),
            'Tase': Decimal('1'),
            'timestamp': datetime.date(2021, 1, 24)
        }

    dict4 = {
            'afds': Decimal( '1'),
            'Käteisnostot': Decimal('7'),
            'Tulot yht.': Decimal('-6'),
            'Muut tulot': Decimal('1'),
            'Menot yht.': Decimal('8'),
            'Muut menot': Decimal('-9'),
            'Tase': Decimal('9'),
            'timestamp': datetime.date(2020, 12, 24)
        }

    expected = [dict1, dict2, dict3, dict4]

    actual = handler.read_in_time_period(START_DATE)
    assert expected == actual

def test_read_from_date_to_date(handler):
    dict1 = {
            'afds': Decimal('2'),
            'Käteisnostot': Decimal('7'),
            'Tulot yht.': Decimal ('9'),
            'Muut tulot': Decimal('-20'),
            'Menot yht.': Decimal('6'),
            'Muut menot': Decimal('-1'), 'Tase': Decimal('6'),
            'timestamp': datetime.date(2021, 2, 24)
        }

    dict2 = {
            'afds': Decimal('3'),
            'Käteisnostot': Decimal ('-1'),
            'Tulot yht.': Decimal('3'),
            'Muut tulot': Decimal('-6'),
            'Menot yht.': Decimal('14'),
            'Muut menot': Decimal('-8'),
            'Tase': Decimal('1'),
            'timestamp': datetime.date(2021, 1, 24)
        }

    dict3 = {
            'afds': Decimal( '1'),
            'Käteisnostot': Decimal('7'),
            'Tulot yht.': Decimal('-6'),
            'Muut tulot': Decimal('1'),
            'Menot yht.': Decimal('8'),
            'Muut menot': Decimal('-9'),
            'Tase': Decimal('9'),
            'timestamp': datetime.date(2020, 12, 24)
        }

    expected = [dict1, dict2, dict3]
    actual = handler.read_in_time_period(START_DATE, END_DATE)
    assert expected == actual
