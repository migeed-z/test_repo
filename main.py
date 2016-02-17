from player import Player
from dealer import Dealer
from random import choice
from retic import Void,List,Tuple

def generate_dealer(players:List(Player))->Dealer:
    """
    Instantiates the dealer which will take over the game
    :return: Dealer
    """
    points = [0 for i in range(len(players))]
    return Dealer(players, points)

def generate_players(num_players:int)->List(Player):
    """
    instantiates n players with an empty list of cards
    :param num_players: int
    :return: [Players...]
    """
    strats_list = [min, max]
    players = []
    for i in range(num_players):
        players.append(Player(i, [], choice(strats_list)))
    return players

def main()->Void:
    try:
        num = int(input('Input:'))
        turns = 9
        cards_per_player = 10
        cards_per_game = 210

        if num < 2:
            print('Too few players!')

        if cards_per_game/cards_per_player < num:
            print("Too many players!")
            exit()

        players = generate_players(num)
        dealer = generate_dealer(players)
        print("scores: %s" % dealer.simulate_game(turns,
                                                  6,
                                                  cards_per_game,
                                                  order=.5,
                                                  bull_points=.5))
    except ValueError:
        print("Not a number")
main()