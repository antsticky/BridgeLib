from project.base.board import Board
from project.analytics.dds import DDSolver
from project.base.people import Team, Player

from project.base.board import Deck


def define_players():
    RR = Team("RR", 666)

    Zsuzsa = Player("Zsuzsa", "Réti Zsuzsa", team=RR)
    Gyorgy = Player("Gyorgy", "Ferenci Gyorgy", team=RR)

    Andi = Player("Andi", "Sinkovicz Andrea", team=RR)
    Peter = Player("Peter", "Sinkovicz Péter", team=RR)

    return Andi, Peter, Zsuzsa, Gyorgy

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
    
    return variable


if __name__ == "__main__":
    N_player, S_player, E_player, W_player = define_players()

    load_mode = validate_input(
        question="\nDo you want to use random or saved boards? [r/s] ",
        error_msgs=['Please select either "r" or "s".'],
        conditions=[load_mode_check],
    )
    #nb_boards = input("How many boards do you want to play? ")

    cum_sum_point = 0
    your_cum_sum_point = 0
    for i in range(20):
        board = Board(board_nb=i + 1)
        board.seating(N=N_player, S=S_player, E=E_player, W=W_player)
        
        if load_mode == "s":
            try:
                board.load_deck(file_name="misc/boards.txt", line_idx=i)
            except IndexError:
                print("\nNo more board to load...")
                break
        else:
            board.deal()


        optimal = DDSolver.get_par_score(deck=board.deck, vul=board.is_vul, is_print=False)

        print(f'{"=" * 40}\n{optimal.get("declarer")}: {optimal.get("contract")} NS/EW: {board.is_vul["N"]}/{board.is_vul["E"]}\n')
        opener = Deck.show_opener_hand(board, optimal["declarer"])

        test_lead = validate_input(
            question="\nWhat is your opening lead? ",
            error_msgs=[
                'Wrong format, please use short suit code and rank, e.g.: "H3"',
                'Your are not holding this card',
                ],
            conditions=[
                card_format_check,
                is_holding_check,
                ],
            opener=opener,
            deck=board.deck,
        )

        board.deck.show()

        trump_suit = "NT" if optimal["contract"][1] == "N" else optimal["contract"][1]
        lead_scores, best_score, worst_score, _ = DDSolver.score_leads(deck=board.deck, trump=trump_suit, first=opener)
        lead_score = DDSolver.get_lead_score(lead_scores, test_lead, is_print=True)

        max_score = best_score - worst_score + 1
        your_score = lead_score - worst_score + 1
        your_cum_sum_point += your_score
        cum_sum_point += max_score
        print(f"\n\nYour score is {your_score} out of {max_score}")
        print(f'Your overall score is {your_cum_sum_point}/{cum_sum_point} = {int(100*your_cum_sum_point/cum_sum_point)}%\n{"=" * 40}')

        is_next = input("\nOne more? [y/n] ")
        if is_next != "y":
            break
