from retic import List,Tuple,Void,String

class Player:
    """
    To represent a player in the game
    """
    def __init__(self:Player, name:int, cards:List(Tuple(int,int)), strat)->Void:
        """
        :param name: Int
        :param cards: [Tuple...]
        :param strat: Function, to be called on face values of cards
        :return: Player
        """
        self.name = name
        self.strat = strat
        self.cards = cards

    def discard(self:Player)->int:
        """
        Return index of card to be discarded
        :return: Int
        """
        face_values = list(map(lambda card: card[0], self.cards))
        discarded_index = face_values.index(self.strat(face_values))
        return discarded_index

    def choose_correct_stack(self:Player, stacks:List(List(Tuple(int,int))))->int:
        """
        Returns the index of the correct stack
        :param stacks: [[Tuple ...]...]
        :return: Int
        """
        top_cards = list(map(lambda stack: stack[-1], stacks))
        discarded_index = self.discard()
        discarded = self.cards[discarded_index]
        if discarded[0] < min(list(map(lambda card: card[0], top_cards))):
            return self.pick_smallest_stack(stacks)
        else:
            return self.get_index_of_closest_stack(top_cards, discarded)

    def get_sum(self:Player, stack:List(Tuple(int,int)))->int:
        """
        returns the player's bull points per turn
        :param stack: [Tuples ...]
        :return Int
        """
        bull_points = sum(list(map(lambda card: card[1], stack)))
        return bull_points

    def sum_stacks(self:Player, stacks:List(List(Tuple(int,int))))->List(int):
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

    def get_index_of_closest_stack(self:Player, cards:List(Tuple(int,int)), card:Tuple(int,int))->int:
        """
        gets index of stack closest to card in value
        :param cards: [Tuple ...]
        :return: Int
        """
        diffs = []
        for c in cards:
            diff = abs(card[0] - c[0])
            diffs.append(diff)
        return diffs.index(min(diffs))

    def pick_smallest_stack(self:Player, stacks:List(List(Tuple(int,int))))->int:
        """
        returns the index of the stack with the smallest value
        :param stacks: [[Tuple ...] ...]
        :return: int
        """
        sums = self.sum_stacks(stacks)
        return sums.index(min(sums))

    def take_hand(self:Player, hand:List(Tuple(int,int)))->Void:
        """
        Updates players' hand
        :param hand: [Tuple ...]
        :return: None
        """
        self.cards = hand

    def __str__(self:Player)->String:
        return "name: %s, cards: %s"\
               %(self.name,
                 [str(card) for card in self.cards])