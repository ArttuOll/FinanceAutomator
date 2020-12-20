"""Sisältää yksikkötestit luokalle ReportCalculator."""
import datetime
from decimal import Decimal

import pytest

from ..util.report_operations import average_reports, sum_reports


@pytest.fixture
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
            'Muut menot': Decimal('-1'),
            'Tase': Decimal('6'),
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

def test_sum_reports(_get_reports):
    expected = {
            'afds': Decimal('3'),
            'Käteisnostot': Decimal('16'),
            'Tulot yht.': Decimal('4'),
            'Muut tulot': Decimal('-21'),
            'Menot yht.': Decimal('31'),
            'Muut menot': Decimal('-16'),
            'Tase': Decimal('18'),
        }

    actual = sum_reports(_get_reports)
    assert expected == actual

def test_average_reports(_get_reports):
    expected = {
            'afds': Decimal('0.75'),
            'Käteisnostot': Decimal('4'),
            'Tulot yht.': Decimal('1'),
            'Muut tulot': Decimal('-5.25'),
            'Menot yht.': Decimal('7.75'),
            'Muut menot': Decimal('-4'),
            'Tase': Decimal('4.5'),
        }

    actual = average_reports(_get_reports)
    assert expected == actual
