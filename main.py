from player import Player
from dealer import Dealer
from retic import Void,List

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
    players = []
    for i in range(num_players):
        players.append(Player(i, []))
    return players

def main()->Void:
    try:
        num = int(input('Input:'))
        turns = 10
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
                                                  5,
                                                  cards_per_game,
                                                  order=.5,
                                                  bull_points=.5))


    # def simulate_game(self:Dealer,
    #                   turns:int,
    #                   size:int,
    #                   deck_size:int,
    #                   rounds=None,
    #                   bull_points=None,
    #                   order=None)->List(Tuple(int, int)):



    except ValueError:
        print("Not a number")
main()