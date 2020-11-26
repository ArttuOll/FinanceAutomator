"""Sisältää yksikkötestit luokalle ReportCalculator."""
import datetime
from decimal import Decimal

import pytest

from ..model.report_calculator import ReportCalculator


def _get_reports():
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

    return [dict1, dict2, dict3, dict4]

@pytest.fixture()
def handler():
    """Returns a ReportReader instantiated with test parameters."""
    return ReportCalculator()

REPORTS = _get_reports()

def test_sum_reports(handler):
    expected = {
            'afds': Decimal('3'),
            'Käteisnostot': Decimal('16'),
            'Tulot yht.': Decimal('4'),
            'Muut tulot': Decimal('-21'),
            'Menot yht.': Decimal('31'),
            'Muut menot': Decimal('-16'),
            'Tase': Decimal('18'),
        }

    actual = handler.sum_reports(REPORTS)
    assert expected == actual
