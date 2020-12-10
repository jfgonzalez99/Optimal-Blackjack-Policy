from numpy import arange
import pickle

def get_Q_state(state):
    """ 
    Converts a given state to a string where each element in state is separated
    with a hyphen
    """
    state_string = '-'.join(str(e) for e in state)
    return state_string

def init_three_card_Q_table():
    sums = arange(12,22)
    usableAce = arange(2)
    numHighCards = arange(21)
    numMidCards = arange(13)
    numLowCards = arange(21)

    initial_Q_table = {}

    for s in sums:
        for a in usableAce:
            for h in numHighCards:
                for m in numMidCards:
                    for l in numLowCards:
                        state = [s,a,h,m,l]
                        state_string = get_Q_state(state)
                        initial_Q_table[state_string] = [0,0]

    pickle.dump(initial_Q_table, open( "three_card_Q_table.p", "wb" ))

def init_five_card_Q_table():
    sums = arange(12,22)
    usableAce = arange(2)
    num2_3 = arange(9)
    num4_5 = arange(9)
    num6_7 = arange(9)
    num8_9 = arange(9)
    numHighCards = arange(21)

    initial_Q_table = {}

    for s in sums:
        for a in usableAce:
            for h in numHighCards:
                for c1 in num8_9:
                    for c2 in num6_7:
                        for c3 in num4_5:
                            for c4 in num2_3:
                                state = [s,a,h,c1,c2,c3,c4]
                                state_string = get_Q_state(state)
                                initial_Q_table[state_string] = [0,0]

    pickle.dump(initial_Q_table, open( "five_card_Q_table.p", "wb" ))