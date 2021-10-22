from project.base.bid import Bid
from project.base.contract import Contract


if __name__ == "__main__":
    bid_level = 2
    vul = "VUL"
    suits = ["C", "D", "H", "S", "NT"]
    is_dbl = True
    is_rdbl = False

    test_contracts = []
    for suit in suits:
        contract_str = str(bid_level) + suit
        test_contracts.append(Contract("N", Bid(contract_str), is_dbl, is_rdbl, vul))

    for i in range(14):
        print(f"{i})", end="\t")

        for contract in test_contracts:
            value = contract.value(tricks=i)
            print(value, end="\t")

        print(end="\n")
