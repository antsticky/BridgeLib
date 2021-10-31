def load_mode_check(load_mode, **kwargs):
    return load_mode in ["r", "s"]


def card_format_check(test_lead, **kwargs):
    if test_lead is None:
        return False

    if len(test_lead) != 2:
        return False

    if test_lead[0] not in ["C", "D", "H", "S"]:
        return False

    if test_lead[1] not in ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]:
        return False

    return True


def is_holding_check(test_lead, deck, opener, **kwargs):
    hand = getattr(deck, opener.name)

    is_in = False
    for suit, cards in hand.items():
        suit_name = suit.short_name
        for card in cards:
            card_name = card.value.display_name
            if test_lead == suit_name + card_name:
                is_in = True

    return is_in


def validate_input(question, error_msgs, conditions, **kwargs):
    variable = None

    while not all([condition(variable, **kwargs) for condition in conditions]):
        variable = input(question)

        for condition, error_msg in zip(conditions, error_msgs):
            if not condition(variable, **kwargs):
                print(error_msg)
                break

    return variable
