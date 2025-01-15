from schnapsen.game import Bot, Move, PlayerPerspective
# other needed imports here. Most likely you need:
from schnapsen.game import SchnapsenTrickScorer
from schnapsen.deck import Card, Suit, Rank


class passive(Bot):
    """Your suit order is [HEARTS, CLUBS, DIAMONDS, SPADES], from lower suit to higher suit."""


    def get_move(self, perspective: PlayerPerspective, leader_move: Move | None) -> Move:
        """Get the move for the Bot.
        The basic structure for your bot is already implemented and must not be modified.
        To implement your bot, only modify the condition and action methods below.
        """
        if self.condition1(perspective, leader_move):
            return self.action1(perspective, leader_move)
        elif self.condition2(perspective, leader_move):
            if self.condition3(perspective, leader_move):
                return self.action2(perspective, leader_move)
            else:
                return self.action3(perspective, leader_move)
        else:
            return self.action4(perspective, leader_move)

    def condition1(self, perspective: PlayerPerspective, leader_move: Move | None) -> bool:
        valid_moves = perspective.valid_moves()
        for move in valid_moves:
            if move.is_marriage():
                marriage = move.as_marriage()
                if marriage.suit == Suit.HEARTS:
                    return True
        return False

    def condition2(self, perspective: PlayerPerspective, leader_move: Move | None) -> bool:
        """2. otherwise, if the 🂱 (ACE_HEARTS) has not been won yet by either bot [1 point]"""
        played_cards = perspective.get_won_cards()
        played_cards2 = perspective.get_opponent_won_cards()
        if Card.ACE_HEARTS not in played_cards and Card.ACE_HEARTS not in played_cards2:
            return True
        return False
            
    def condition3(self, perspective: PlayerPerspective, leader_move: Move | None) -> bool:
        hand = perspective.get_hand()
    
        if len(hand) < 1:
            return False
            
        points = SchnapsenTrickScorer()
        points_sum = 0
        all_cards = 0
        
        for card in hand.get_cards():
            points2 = points.rank_to_points(card.rank)
            points_sum += points2
            all_cards += 1

        average = points_sum / all_cards
        if average < 8.0:
            return True
        return False

    def action1(self, perspective: PlayerPerspective, leader_move: Move | None) -> Move:
        """   then play the HEARTS marriage  [1.5 point]"""
        valid_moves = perspective.valid_moves()
    
        for move in valid_moves:
            if move.is_marriage():
                marriage = move.as_marriage()
                if marriage.suit == Suit.HEARTS:
                    return move

    def action2(self, perspective: PlayerPerspective, leader_move: Move | None) -> Move:
        """                     then play the valid regular move where the card has the lowest suit according
                          to the suit order above. If multiple cards have the lowest suit,
                          prioritize according to lowest points. [1.5 points]"""
        moves = perspective.valid_moves()
        
        hearts_moves = []
        clubs_moves = []
        diamonds_moves = []
        spades_moves = []

        for move in moves:
            if not move.is_regular_move():  
                continue
            card = move.as_regular_move().card
            if card.suit == Suit.HEARTS:
                hearts_moves.append(move)
            elif card.suit == Suit.CLUBS:
                clubs_moves.append(move)
            elif card.suit == Suit.DIAMONDS:
                diamonds_moves.append(move)
            else:
                spades_moves.append(move)
    
        scorer = SchnapsenTrickScorer()
        
        if len(hearts_moves) > 0:
            moves = sorted(hearts_moves, key=lambda m: scorer.rank_to_points(m.as_regular_move().card.rank))
            return moves[0]
        elif len(clubs_moves) > 0:
            moves = sorted(clubs_moves, key=lambda m: scorer.rank_to_points(m.as_regular_move().card.rank))
            return moves[0]
        elif len(diamonds_moves) > 0:
            moves = sorted(diamonds_moves, key=lambda m: scorer.rank_to_points(m.as_regular_move().card.rank))
            return moves[0]
        elif len(spades_moves) > 0:
            moves = sorted(spades_moves, key=lambda m: scorer.rank_to_points(m.as_regular_move().card.rank))
            return moves[0]
    
  

    def action3(self, perspective: PlayerPerspective, leader_move: Move | None) -> Move:
        """                  b. otherwise find the most frequent suit among the cards in valid regular moves.
                               If multiple suits have the same most frequency, prioritize according
                               to the suit order above. Among these cards, play the one with the
                               lowest points. [2.0 points]"""
        
        pass

    def action4(self, perspective: PlayerPerspective, leader_move: Move | None) -> Move:
        """3. otherwise take the cards in valid regular moves and order them by points (low to high); in this
             ordering, if two cards have the same points, sort these according to the suit order.
             Now, play the card in the middle of the sequence. If the number of cards is even, play
             the card right below the middle. [1.5 points]"""
        moves = perspective.valid_moves()
        scorer = SchnapsenTrickScorer()
        
        sorted_moves = []
        for move in moves:
            if move.is_regular_move():
                card = move.as_regular_move().card
                points = scorer.rank_to_points(card.rank)
                suit_value = [Suit.HEARTS, Suit.CLUBS, Suit.DIAMONDS, Suit.SPADES].index(card.suit)
                sorted_moves.append([points, suit_value, move])
        
        new_sorted_moves = sorted(sorted_moves, key=lambda x: (x[0], x[1]))
        middle_index = (len(new_sorted_moves) - 1) // 2
        return new_sorted_moves[middle_index][2]
