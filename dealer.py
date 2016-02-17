from random import randrange, shuffle, random, seed
from copy import deepcopy
from player import Player
from retic import List, Void, Tuple, Bool

min_val = 2
max_val = 7

class Dealer:
    """
    To represent the Dealer for the whole game
    """

    def __init__(self:Dealer, players:List(Player), bull_points:List(int))->Void:
        """
        :param deck: [Card ...]
        :param players: [Player ...]
        :param bull_points: [Int ...]
        """
        self.deck = []
        self.players = players
        self.bull_points = bull_points

    def simulate_game(self:Dealer,
                      min:int,
                      max:int,
                      turns:int,
                      size:int,
                      deck_size:int,
                      rounds=None,
                      bull_points=None,
                      order=None)->List(Tuple(int, int)):
        """
        Similulates a game and returns the players' scores
        :param min: Int
        :param max: Int
        :param turns: Int
        :param deck_size: Int
        :param size: Int, take stack if len(stack) == size
        :param rounds: Int or None
        :param bull_points: float
        :param order: float between 0 and 1
        :return: [Tuple ...]
        """

        var = 0
        while not self.is_over():
            self.simulate_round(min, max, turns, size, deck_size, bull_points, order)
            if rounds == var:
                break
            else: var+=1
        return self.output_scores()

    def simulate_round(self:Dealer,
                       min:int,
                       max:int,
                       turns:int,
                       size:int,
                       deck_size:int,
                       bull_points=None,
                       order=None)->Void:
        """
        Simulates a complete round of 10 turns
        :param min: Int
        :param max: Int
        :param turns: Int
        :param deck_size: Int
        :param size: Int, take stack if len(stack) == size
        :param bull_points: float
        :param order: float between 0 and 1
        :return: None
        """
        self.create_deck(deck_size, min, max, bull_points, order)
        self.hand()
        stacks = self.create_stacks()
        for i in range(turns):
            for j in range(len(self.players)):
                player = self.players[j]
                chosen_stack_index = player.choose_correct_stack(stacks)
                (p, s) = self.update_game(player, chosen_stack_index, stacks, size)
                self.bull_points[j]+=p
                stacks = s

    def create_deck(self:Dealer, deck_size:int, min:int, max:int, bull_points=None, order=None)->Void:
        """
        :param deck_size: Int, number of cards in deck
        :param min: Int, minimum number of bull points
        :param max: Int, maximum number of bull points
        :param bull_points: float, bull points parametrization
        :param order: float, order of cards parametrization
        :return: [Card ...]
        """
        seed(bull_points)
        cards = []
        if min >= max:
            raise ValueError('min less than max')
        for i in range(deck_size):
            cards.append((i+1, randrange(min, max)))
        s = (order or random())
        shuffle(cards, lambda: s)
        self.deck = cards

    def hand(self:Dealer)->Void:
        """
        Hand cards to players and update deck and players' cards
        accordingly
        :return: None
        """
        for player in self.players:
            hand = self.deck[:10]
            player.take_hand(hand)
            del self.deck[:10]

    def create_stacks(self:Dealer)->(List(List(Tuple(int, int)))):
        """
        create 4 new stacks each having 1 card from the deck
        at the start of every round
        Initialize all players with that stack
        :return: [[Tuple] ...]
        """
        stacks = []
        for i in range(4):
            stacks.append([self.deck.pop()])
        return stacks

    def is_over(self:Dealer)->Bool:
        """
        Is the game over?
        :return: Boolean
        """
        return max(self.bull_points) >= 66

    def output_scores(self:Dealer)->List(Tuple(int, int)):
        """
        Outputs the names of the winning and losing players
        :param players: [Player ...]
        :return: (Player, Player)
        """
        res = []
        for i in range(len(self.players)):
            player_points = self.bull_points[i]
            player_name = self.players[i].name
            res.append((player_name, player_points))
        return res

    def update_game(self:Dealer, player:Player, stack_index:int, stacks:List(List(Tuple(int, int))), size:int)->\
            Tuple(int, List(List(Tuple(int, int)))):
        """
        update playe's bull points based on chosen stack
        :param stack_index: Int
        :param stacks: [[Tuple...]...] where len(stacks)=4
        :param size: Int, take stack if len(stack) == size
        :return: Tuple
        """
        top_cards = list(map(lambda stack: stack[-1], stacks))
        discarded_index = player.discard()
        discarded = player.cards.pop(discarded_index)

        if discarded[0] < min(list(map(lambda card: card[0], top_cards))):
            bull_points = self.get_sum(stacks[stack_index])

            new_stacks = self.replace_card(discarded, stack_index, stacks)
            return bull_points, new_stacks

        else:
            my_stack = stacks[stack_index]
            if len(my_stack) == size:
                bull_points = self.get_sum(my_stack)
                new_stacks = self.replace_card(discarded, stack_index, stacks)
                return (bull_points, new_stacks)
            else:
                new_stacks = self.add_card(discarded, stack_index, stacks)
                return 0, new_stacks

    def get_sum(self:Dealer, stack:List(Tuple(int, int)))->int:
        """
        returns the player's bull points per turn
        :param stack: [Tuples ...]
        :return Int
        """
        bull_points = sum(list(map(lambda card: card[1], stack)))
        return bull_points

    def replace_card(self:Dealer, card:Tuple(int, int), index:int, stacks:List(List(Tuple(int, int))))->List(List(Tuple(int, int))):
        """
        Replaces stack with card and returns new stack
        :param card: Tuple
        :param index: Int
        :param stacks: [[Tuples ...] ...]
        :return [[Tuple...]...]
        """
        new_stacks = deepcopy(stacks)
        new_stacks[index] = [card]
        return new_stacks

    def sum_stacks(self:Dealer, stacks:List(List(Tuple(int, int))))->List(int):
        """
        Sums the bull points of stacks
        :param stacks [[Tuple ...] ...] where len(stacks)=4
        :return: [Int, ...]
        """
        sums = []
        for stack in stacks:
            bull_points = list(map(lambda card: card[1], stack))
            sums.append(sum(bull_points))
        return sums

    def add_card(self:Dealer, card:Tuple(int, int), index:int, stacks:List(List(Tuple(int, int))))->List(List(Tuple(int, int))):
        """
        adds card on top of the stack[index]
        :param card: Tuple
        :param stack: [Tuple...]
        :return: [Tuple...]
        """
        new_stacks = deepcopy(stacks)
        new_stacks[index].append(card)
        return new_stacks
