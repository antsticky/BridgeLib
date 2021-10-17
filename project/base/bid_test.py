import pytest

from project.base.bid import Contract, Bid

@pytest.mark.parametrize(
    "test_input",
    [
        (1,"VUL", ["C", "D"], False, False),
        (3,"VUL", ["C", "D"], False, False),
        (6,"VUL", ["C", "D"], False, False),
        (7,"VUL", ["C", "D"], False, False),
        (2,"VUL", ["H", "S"], False, False),
        (5,"VUL", ["H", "S"], False, False),
        (6,"VUL", ["H", "S"], False, False),
        (7,"VUL", ["H", "S"], False, False),
    ],
)
def test_get_day_fullname(test_input):
    bid_level, vul, suits, is_dbl, is_rdbl = test_input

    test_contracts = []
    for suit in suits:
        contract_str = str(bid_level) + suit
        test_contracts.append(Contract("N", Bid(contract_str), is_dbl, is_rdbl, vul))

    for i in range(14):
        assert test_contracts[0].value(tricks=i) == test_contracts[1].value(tricks=i)

    