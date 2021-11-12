import random
import itertools

all_ranks = '23456789TJQKA'
black_cards = [r+s for r in all_ranks for s in 'SC']
red_cards = [r+s for r in all_ranks for s in 'HD']
my_deck = [r+s for r in '23456789TJQKA' for s in 'SHDC']


count_rankings = {
    (5,): 10,
    (4, 1): 7,
    (3, 2): 6,
    (3, 1, 1): 3,
    (2, 2, 1): 2,
    (2, 1, 1, 1): 1,
    (1, 1, 1, 1, 1): 0
}

hand_names = {
    0: "High Card",
    1: "Pair",
    2: "2 Pair",
    3: "3 Kind",
    4: "Straight",
    5: "Flush",
    6: "Full House",
    7: "4 Kind",
    8: "Straight Flush",
    9: "5 Kind"
}


def best_hand(hand: list) -> list:
    """From a 7-card hand, return the best 5-card hand."""
    return max(itertools.combinations(hand, 5), key=hand_rank)


def best_wild_hand(hand: list) -> list:
    """Try all values for jokers in all 5-card selections."""
    hands = set(best_hand(h) 
                for h in itertools.product(*map(replacements, hand)))
    
    return max(hands, key=hand_rank)


def replacements(card: str) -> list:
    """
    Return a list of possible replacements for a card.
    There will be more than 1 only for wild cards.
    """
    if card == '?B':
        return black_cards
    elif card == '?R':
        return red_cards
    else:
        return [card]


def deal(num_hands, n=5, deck=my_deck) -> list[list]:
    """Shuffle the deck and deal out num_hands n-card hands."""
    random.shuffle(deck)

    return [deck[n*i:n*(i+1)] for i in range(num_hands)]


def poker(hands: list[list]) -> list[list]:
    """
    Return a list of winning hands: 
    poker([hand, ...]) -> [hand, ...]
    """
    return all_max(hands, key=hand_rank)


def all_max(iterable, key=None) -> list:
    """Return a list of all items equal to the max of the iterable."""
    result, max_value = [], None
    key = key or (lambda x: x)
    for x in iterable:
        xval = key(x)
        if not result or xval > max_value:
            result, max_value = [x], xval
        elif xval == max_value:
            result.append(x)

    return result


def hand_rank(hand: list) -> tuple:
    """Return a value indicating the ranking of a hand."""
    groups = group(['--23456789TJQKA'.index(r) for r,s in hand])
    # counts is the count of each rank; ranks lists corresponding ranks
    counts, ranks = unzip(groups)

    if ranks == (14, 5, 4, 3, 2):
        ranks = (5, 4, 3, 2, 1)

    straight = len(set(ranks)) == 5 and max(ranks) - min(ranks) == 4
    flush = len(set([s for r,s in hand])) == 1

    return max(count_rankings[counts], 4*straight + 5*flush), ranks


def group(items: list) -> list[tuple]:
    """
    Returns a list of [(count, x)...], highest count first, then
    highest x first.
    """
    groups = [(items.count(x), x) for x in set(items)]

    return sorted(groups, reverse=True)


def unzip(pairs: list[tuple]): return zip(*pairs)


def hand_percentages(n=700*1000):
    """
    Sample n random hands and print a table of percentages for each
    type of hand.
    """
    counts = [0] * 9

    for i in range(n//10):
        for hand in deal(10):
            ranking = hand_rank(hand)[0]
            # Adjust straight flush ranking
            if ranking == 9:
                ranking -=1
            counts[ranking] += 1

    for i in reversed(range(9)):
        print(f"{hand_names[i]:>14}: {100*counts[i]/n:6.3f} %")


def test():
    "Test cases for the functions in poker program"
    sf = "6C 7C 8C 9C TC".split() # Straight flush
    fk = "9D 9H 9S 9C 7D".split() # Four of a kind
    fh = "TD TC TH 7C 7D".split() # Full House
    tp = "5S 5D 9H 9C 6S".split() # Two pairs
    al = "AC 2D 4H 3D 5S".split() # Ace-Low Straight 
    
    assert hand_rank(sf) == (9, (10, 9 , 8, 7, 6))
    assert hand_rank(fk) == (7, (9, 7))
    assert hand_rank(fh) == (6, (10 ,7))
    assert hand_rank(tp) == (2, (9, 5, 6))
    assert hand_rank(al) == (4, (5, 4, 3, 2, 1))

    assert poker([sf, fk, fh]) == [sf]
    assert poker([fk, fh]) == [fk]
    assert poker([fh, fh]) == [fh, fh]
    assert poker([fh]) == [fh]
    assert poker([sf] + 99 * [fh]) == [sf]

    return "tests pass"


def test_best_hand():
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])

    return 'test_best_hand passes'


def test_best_wild_hand():
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])

    return 'test_best_wild_hand passes'
