import pytest

from project.base.bid import Contract, Bid


@pytest.mark.parametrize(
    "bid_level,vul,suits,is_dbl,is_rdbl",
    [
        (1, "VUL", ["C", "D"], False, False),
        (3, "VUL", ["C", "D"], False, False),
        (6, "VUL", ["C", "D"], False, False),
        (7, "VUL", ["C", "D"], False, False),
        (2, "VUL", ["H", "S"], False, False),
        (5, "VUL", ["H", "S"], False, False),
        (6, "VUL", ["H", "S"], False, False),
        (7, "VUL", ["H", "S"], False, False),
    ],
)
def test_minor_major_plain(bid_level, vul, suits, is_dbl, is_rdbl):
    test_contracts = []
    for suit in suits:
        contract_str = str(bid_level) + suit
        test_contracts.append(Contract("N", Bid(contract_str), is_dbl, is_rdbl, vul))

    for i in range(14):
        assert test_contracts[0].value(tricks=i) == test_contracts[1].value(tricks=i)


@pytest.mark.parametrize(
    "bid_level,vul,suits,is_dbl,is_rdbl",
    [
        (1, "VUL", ["C", "D"], True, False),
        (3, "VUL", ["C", "D"], True, False),
        (6, "VUL", ["C", "D"], True, False),
        (7, "VUL", ["C", "D"], True, False),
        (2, "VUL", ["H", "S"], True, False),
        (5, "VUL", ["H", "S"], True, False),
        (6, "VUL", ["H", "S"], True, False),
        (7, "VUL", ["H", "S"], True, False),
    ],
)
def test_minor_major_dbl(bid_level, vul, suits, is_dbl, is_rdbl):
    test_contracts = []
    for suit in suits:
        contract_str = str(bid_level) + suit
        test_contracts.append(Contract("N", Bid(contract_str), is_dbl, is_rdbl, vul))

    for i in range(14):
        assert test_contracts[0].value(tricks=i) == test_contracts[1].value(tricks=i)


@pytest.mark.parametrize(
    "bid_level,vul,suits,is_dbl,is_rdbl",
    [
        (1, "VUL", ["C", "D"], False, True),
        (3, "VUL", ["C", "D"], False, True),
        (6, "VUL", ["C", "D"], False, True),
        (7, "VUL", ["C", "D"], False, True),
        (2, "VUL", ["H", "S"], False, True),
        (5, "VUL", ["H", "S"], False, True),
        (6, "VUL", ["H", "S"], False, True),
        (7, "VUL", ["H", "S"], False, True),
    ],
)
def test_minor_major_rdbl(bid_level, vul, suits, is_dbl, is_rdbl):
    test_contracts = []
    for suit in suits:
        contract_str = str(bid_level) + suit
        test_contracts.append(Contract("N", Bid(contract_str), is_dbl, is_rdbl, vul))

    for i in range(14):
        assert test_contracts[0].value(tricks=i) == test_contracts[1].value(tricks=i)