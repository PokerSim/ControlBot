import pokerkit as pk
import itertools

#global variables
chip_count = 0
hand = []

#determine the next action to take
# vars needed: current_bet, community_cards, hand, chip_count, num_players, position
def take_action(current_bet, community_cards):
    result = ""
    if result == "R": return "raise"
    elif result == "C": return "call"
    elif result == "F": return "fold"
    else: return "fold"

#determine what to do postflop
def postflop_action(numPlayers, playerIndex, current_bet, community_cards, pot_size):
    global hand, chip_count
    
    # Create a hand object
    hole_cards = pk.Hand(*hand)
    board = pk.Board(*community_cards)
    
    # Evaluate hand strength
    strength = pk.evaluate(hole_cards, board)
    
    # Calculate pot odds
    call_cost = current_bet - (chip_count if chip_count < current_bet else 0)
    pot_odds = call_cost / (pot_size + call_cost) if call_cost > 0 else 0
    
    # Example strategy
    if strength > 0.8:  # Strong hand, aggressive play
        return "R"
    elif strength > 0.5:  # Decent hand, call if odds are good
        return "C" if pot_odds <= 0.5 else "F"
    else:  # Weak hand
        return "F"
    
#determine what to do preflop
def preflop_action(numPlayers, playerIndex, been_raised, are_limpers):
    column = determine_position(numPlayers, playerIndex)
    if been_raised(): column += 6
    if are_limpers(): column += 3

    rows = {"AAo": 0, "KKo": 0, "QQo": 0, 
            "JJo": 1,
            "TTo": 2,
            "99o": 3, "88o": 3, "77o": 3,
            "66o": 4, "55o": 4, "44o": 4, "33o": 4, "22o": 4,
            "AKo": 5, "AKs": 5,
            "AQo": 6, "AQs": 6,
            "AJo": 7, "AJs": 7, "ATs": 7, "KQo": 7, "KJo": 7, "KQs": 7, "KJs": 7, "QJs": 7, "JTs": 7,
            "ATo": 8, "KTs": 8,
            "A9s": 9, "A8s": 9, "KTo": 9, "K9s": 9, "QJo": 9, "QTo": 9, "QTs": 9, "J9s": 9, "T9s": 9, "98s": 9,
            "A9o": 10, "A8o": 10, "A7s": 10, "A6s": 10, "A5s": 10, "A4s": 10, "A3s": 10, "A2s": 10, "K9o": 10, "Q9s": 10, "JTo": 10, "J8s": 10, "T9o": 10, "T8s": 10, "98o": 10, "97s": 10, "87s": 10, "86s": 10, "76s": 10, "65s": 10,
            "A7o": 11, "A6o": 11, "A5o": 11, "A4o": 11, "A3o": 11, "A2o": 11, "K8s": 11, "Q9o": 11, "Q8s": 11, "J9o": 11, "J8o": 11, "J7s": 11, "T8o": 11, "T7s": 11, "T6s": 11, "97o": 11, "96s": 11, "87o": 11, "75s": 11, "54s": 12}

    if hand[0][1] == hand[1][1]:
        hand_str = hand[0][0] + hand[1][0] + "s"
    else:
        hand_str = hand[0][0] + hand[1][0] + "o"
    row = rows.get(hand_str, None)
    if row is None:
        return "fold"

    solutions = [[['R'], ['R'], ['R'], ['R'], ['R'], ['R'], ['R'], ['R'], ['R']],
                 [['R'], ['R'], ['R'], ['R'], ['R'], ['R'], ['C'], ['C'], ['R']],
                 [['R'], ['R'], ['R'], ['R'], ['R'], ['R'], ['C'], ['C'], ['C']],
                 [['R'], ['R'], ['R'], ['C'], ['R'], ['R'], ['C'], ['C'], ['C']],
                 [['R'], ['R'], ['R'], ['C'], ['C'], ['C'], ['C'], ['C'], ['C']],
                 [['R'], ['R'], ['R'], ['R'], ['R'], ['R'], ['R'], ['R'], ['R']],
                 [['R'], ['R'], ['R'], ['R'], ['R'], ['R'], ['C'], ['R'], ['R']],
                 [['R'], ['R'], ['R'], ['R'], ['R'], ['R'], ['C'], ['C'], ['R']], 
                 [['F'], ['R'], ['R'], ['R'], ['R'], ['R'], ['F'], ['C'], ['C']],
                 [['F'], ['R'], ['R'], ['R'], ['R'], ['R'], ['F'], ['F'], ['C']],
                 [['F'], ['F'], ['R'], ['F'], ['R'], ['R'], ['F'], ['F'], ['F']],
                 [['F'], ['F'], ['R'], ['F'], ['F'], ['F'], ['F'], ['F'], ['F']]]
    
    return solutions[row][column]

# determine position
# 0 == early, 1 == mid, 2 == late, -1 == invalid
def determine_position(numPlayers, playerIndex):
    if (playerIndex == 0 & numPlayers != 2):
        return 2
    #switch case for numPlayers
    match numPlayers:
        case 2:
            return 2
        case 3:
            if playerIndex == 1: return 2
            elif playerIndex == 2: return 1
            else: return -1
        case 4:
            if playerIndex == 1: return 1
            elif playerIndex == 2 | playerIndex == 3: return 0
            else: return -1
        case 5:
            if playerIndex >= 1 & playerIndex <= 3: return 0
            elif playerIndex == 4: return 1
            else: return -1
        case 6:
            if playerIndex >= 1 & playerIndex <= 3: return 0
            elif playerIndex == 4: return 1
            elif playerIndex == 5: return 2
            else: return -1
        case 7:
            if playerIndex >= 1 & playerIndex <= 3: return 0
            elif playerIndex == 4 | playerIndex == 5: return 1
            elif playerIndex == 6: return 2
            else: return -1
        case 8:
            if playerIndex >= 1 & playerIndex <= 4: return 0
            elif playerIndex == 5 | playerIndex == 6: return 1
            elif playerIndex == 7: return 2
            else: return -1
        case 9:
            if playerIndex >= 1 & playerIndex <= 4: return 0
            elif playerIndex == 5 | playerIndex == 6: return 1
            elif playerIndex == 7 | playerIndex == 8: return 2
            else: return -1
        case 10:
            if playerIndex >= 1 & playerIndex <= 5: return 0
            elif playerIndex == 6 | playerIndex == 7: return 1
            elif playerIndex == 8 | playerIndex == 9: return 2
            else: return -1
        case _:
            return "invalid"

#recieve card 
def recieve_card(card):
    hand.append(card)

#add chips to the player's stack
def add_chips(chips):
    global chip_count
    chip_count += chips

#reset the player's chip count
def reset_chips():
    global chip_count
    chip_count = 0

