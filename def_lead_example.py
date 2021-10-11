import project.analytics.requests as loveRequests

SEAT_DICT = {"N": "NORTH", "S": "SOUTH", "W": "WEST", "E": "EAST"}

COLOR_DICT = {"C": "CLUB", "D": "DIAMOND", "H": "HEART", "S": "SPADE", "N": "NT"}

PREV_PLAYER_DICT = {"N": "W", "E": "N", "S": "E", "W": "S"}

TOTAL_TRICKS = 13


def get_board_NS_team_id_player(player, freq):
    if player.room == "open":
        return freq.registrations["HOME"]
    elif player.room == "closed":
        return freq.registrations["VISITING"]

    raise KeyError("Room cannot be found")


def get_room_by_player(player, freq):
    room = None
    if player.playerId in freq.closedEw + freq.closedNs:
        room = "closed"
    elif player.playerId in freq.openEw + freq.openNs:
        room = "open"
    else:
        raise KeyError("Player does not played")

    return room


def get_player_seat(player, freq):
    seat = None
    if player.playerId in freq.closedEw + freq.openEw:
        idx = (freq.openEw + freq.closedEw).index(player.playerId)
        seat = "E" if idx % 2 == 0 else "W"
    elif player.playerId in freq.closedNs + freq.openNs:
        idx = (freq.openNs + freq.closedNs).index(player.playerId)
        seat = "N" if idx % 2 == 0 else "S"
    else:
        raise KeyError("Player does not played")

    return seat


def get_direction_by_player(player, freq):
    direction = None
    if player.playerId in freq.closedEw + freq.openEw:
        direction = ["E", "W"]
    elif player.playerId in freq.closedNs + freq.openNs:
        direction = ["N", "S"]
    else:
        raise KeyError("Player does not played")

    return direction


def check_open_lead(player, freq, board):
    contract, decl, *_ = get_board_result_by_player(player=player, freq=freq)
    dec_aim_score = board.optimumScores.get("maxTricks").get(SEAT_DICT.get(decl)).get(COLOR_DICT.get(contract[-1]))
    prev_player = PREV_PLAYER_DICT.get(player.seat)

    if decl == prev_player:
        print(f"{board.boardNumber}) {player.name} lead")

        dds = loveRequests.DDS.get_by_trick(dds_code=player.NS_team_id, bd_nb=board.boardNumber)

        max_results = -TOTAL_TRICKS
        for poss in dds.solvedCards:
            if poss.get("second") > max_results:
                max_results = poss.get("second")

        try:
            max_possible_trick = 6 + int(contract[0:-1]) + max_results
        except:
            max_possible_trick = 6 + int(contract[0:-2]) + max_results

        print(f"possible tricks (initially) = {dec_aim_score}")
        print(f"possible tricks (after lead)= {max_possible_trick}")

        return dec_aim_score, max_possible_trick

    return None


def get_board_result_by_player(player, freq):
    room = get_room_by_player(player=player, freq=freq)
    direction = get_direction_by_player(player=player, freq=freq)

    if room == "open":
        result = freq.openResult
    elif room == "closed":
        result = freq.closedResult
    else:
        raise KeyError("Player does not played")

    contract = result.get("contract")
    if contract[-1] == "x":
        contract = contract[0:-1]

    score = result.get("score", -1)
    decl = result.get("decl")

    mlplr = 1 if "N" in direction else -1

    return contract, decl, score, mlplr


if __name__ == "__main__":
    RR = loveRequests.Team.create_by_name("RR")

    players = [loveRequests.Player.create_by_name(player_name) for player_name in ["Budinszky András", "Talyigás András", "Sinkovicz Péter", "Sinkovicz Andrea"]]

    f = open("misc/def_lead.csv", "w")
    f.write(f"Board;Name;Optimal;After lead;\n")

    nb_boards = 32
    for i in range(nb_boards):

        board_i = loveRequests.Board.create_by_bd_nb(i + 1)  # board misindexing
        optimal_score = board_i.optimumScores.get("score", -1)

        freq_i = loveRequests.Freqi.create_by_team_id(RR.registrationId, i + 1)

        for player in players:
            player.room = get_room_by_player(player=player, freq=freq_i)
            player.seat = get_player_seat(player=player, freq=freq_i)
            player.NS_team_id = get_board_NS_team_id_player(player=player, freq=freq_i)

            res = check_open_lead(player, freq_i, board_i)
            if res is not None:
                dec_aim_tricks, max_possible_trick = res
                f.write(f"{i+1};{player.name};{dec_aim_tricks};{max_possible_trick};\n")

    f.close()
