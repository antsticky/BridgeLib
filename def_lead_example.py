import numpy as np

import bridgeLib.requests as loveRequests

SEAT_DICT = {"N": "NORTH", "S": "SOUTH", "W": "WEST", "E": "EAST"}

COLOR_DICT = {"C": "CLUB", "D": "DIAMOND", "H": "HEART", "S": "SPADE", "N": "NT"}

PREV_PLAYER_DICT = {"N": "W", "E": "N", "S": "E", "W": "S"}


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

    Budinszky_Andras = loveRequests.Player.create_by_name("Budinszky András")
    Talyigas_Andras = loveRequests.Player.create_by_name("Talyigás András")

    #Reti_Zsuzsa = loveRequests.Player.create_by_name("Réti Zsuzsa")
    #Ferenci_Gyorgy = loveRequests.Player.create_by_name("Ferenci György")
    Sinkovicz_Peter = loveRequests.Player.create_by_name("Sinkovicz Péter")
    Sinkovicz_Andrea = loveRequests.Player.create_by_name("Sinkovicz Andrea")

    f = open("def_lead.csv", "w")
    f.write(f"Board;Name;Optimal;After lead;\n")

    nb_boards = 32
    for i in range(nb_boards):

        board_i = loveRequests.Board.create_by_bd_nb(i + 1)  # board misindexing
        optimal_score = board_i.optimumScores.get("score", -1)

        freq_i = loveRequests.Freqi.create_by_team_id(RR.registrationId, i + 1)

        # ================================================
        Budinszky_Andras.room = get_room_by_player(player=Budinszky_Andras, freq=freq_i)
        Talyigas_Andras.room = get_room_by_player(player=Talyigas_Andras, freq=freq_i)

        Sinkovicz_Peter.room = get_room_by_player(player=Sinkovicz_Peter, freq=freq_i)
        Sinkovicz_Andrea.room = get_room_by_player(player=Sinkovicz_Andrea, freq=freq_i)

        Budinszky_Andras.seat = get_player_seat(player=Budinszky_Andras, freq=freq_i)
        Talyigas_Andras.seat = get_player_seat(player=Talyigas_Andras, freq=freq_i)

        Sinkovicz_Peter.seat = get_player_seat(player=Sinkovicz_Peter, freq=freq_i)
        Sinkovicz_Andrea.seat = get_player_seat(player=Sinkovicz_Andrea, freq=freq_i)

        # ================================================

        contract_Andras_i, decl_Andras_i, score_Andras_i, mlplr_Andras_i = get_board_result_by_player(player=Budinszky_Andras, freq=freq_i)
        dec_aim_score_Andras = board_i.optimumScores.get("maxTricks").get(SEAT_DICT.get(decl_Andras_i)).get(COLOR_DICT.get(contract_Andras_i[-1]))
        prev_player_Andras_i = PREV_PLAYER_DICT.get(Budinszky_Andras.seat)
        if decl_Andras_i == prev_player_Andras_i:
            print(f"{i+1}) {Budinszky_Andras.name} lead")
            dds = loveRequests.DDS.get_by_trick(dds_code=1797511, bd_nb=i+1)

            max_results = -13
            for poss in dds.solvedCards:
                if poss.get("second") > max_results:
                    max_results = poss.get("second")
            
            try:
                max_possible_trick = 6 + int(contract_Andras_i[0:-1]) + max_results
            except:
                max_possible_trick = 6 + int(contract_Andras_i[0:-2]) + max_results

            print(dec_aim_score_Andras)
            print(max_possible_trick)

            f.write(f"{i+1};{Budinszky_Andras.name};{dec_aim_score_Andras};{max_possible_trick};\n")

        prev_player_Talycsi = PREV_PLAYER_DICT.get(Talyigas_Andras.seat)
        if decl_Andras_i == prev_player_Talycsi:
            print(f"{i+1}) {Talyigas_Andras.name} lead")

            dds = loveRequests.DDS.get_by_trick(dds_code=1797511, bd_nb=i+1)

            max_results = -13
            for poss in dds.solvedCards:
                if poss.get("second") > max_results:
                    max_results = poss.get("second")
            
            try:
                max_possible_trick = 6 + int(contract_Andras_i[0:-1]) + max_results
            except:
                max_possible_trick = 6 + int(contract_Andras_i[0:-2]) + max_results

            print(dec_aim_score_Andras)
            print(max_possible_trick)
            
            f.write(f"{i+1};{Talyigas_Andras.name};{dec_aim_score_Andras};{max_possible_trick};\n")


        contract_Zsuzsa_i, decl_Zsuzsa_i, score_Zsuzsa_i, mlplr_Zsuzsa_i = get_board_result_by_player(player=Sinkovicz_Peter, freq=freq_i)
        dec_aim_score_Zsuzsa = board_i.optimumScores.get("maxTricks").get(SEAT_DICT.get(decl_Zsuzsa_i)).get(COLOR_DICT.get(contract_Zsuzsa_i[-1]))
        prev_player_Zsuzsa_i = PREV_PLAYER_DICT.get(Sinkovicz_Peter.seat)
        if decl_Zsuzsa_i == prev_player_Zsuzsa_i:
            print(f"{i+1}) {Sinkovicz_Peter.name} lead")
            dds = loveRequests.DDS.get_by_trick(dds_code=1797530, bd_nb=i+1)

            max_results = -13
            for poss in dds.solvedCards:
                if poss.get("second") > max_results:
                    max_results = poss.get("second")
            
            try:
                max_possible_trick = 6 + int(contract_Zsuzsa_i[0:-1]) + max_results
            except:
                max_possible_trick = 6 + int(contract_Zsuzsa_i[0:-2]) + max_results

            print(dec_aim_score_Zsuzsa)
            print(max_possible_trick)

            f.write(f"{i+1};{Sinkovicz_Peter.name};{dec_aim_score_Zsuzsa};{max_possible_trick};\n")


        prev_player_Fernci = PREV_PLAYER_DICT.get(Sinkovicz_Andrea.seat)
        if decl_Zsuzsa_i == prev_player_Fernci:
            print(f"{i+1}) {Sinkovicz_Andrea.name} lead")

            dds = loveRequests.DDS.get_by_trick(dds_code=1797530, bd_nb=i+1)

            max_results = -13
            for poss in dds.solvedCards:
                if poss.get("second") > max_results:
                    max_results = poss.get("second")

            try:            
                max_possible_trick = 6 + int(contract_Zsuzsa_i[0:-1]) + max_results
            except:
                max_possible_trick = 6 + int(contract_Zsuzsa_i[0:-2]) + max_results

            print(dec_aim_score_Zsuzsa)
            print(max_possible_trick)

            f.write(f"{i+1};{Sinkovicz_Andrea.name};{dec_aim_score_Zsuzsa};{max_possible_trick};\n")

    f.close()
