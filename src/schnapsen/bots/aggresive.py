from schnapsen.game import Bot, Move, PlayerPerspective, GamePhase
from schnapsen.game import SchnapsenTrickScorer
from schnapsen.deck import Card, Suit, Rank


class RiskTakingBot(Bot):
    """
    Schnapsen bot, with a risk taking strategy.
    Playing the high cards first in order to win the game as quick as possible.
    """

    def get_move(self, perspective: PlayerPerspective, leader_move: Move | None) -> Move:

        if leader_move == None:
            return self.get_highest_scoring_move(perspective, leader_move)
        else:
            return self.follow_suit(perspective, leader_move)

    def get_highest_scoring_move(self, perspective: PlayerPerspective, leader_move: Move | None) -> Move:
        """
        If we have the first move we should play the moves with the highest points:
        First marriage, then trump, and then the cards with the highest points.
        """
        scorer = SchnapsenTrickScorer()
        moves = perspective.valid_moves()
        trump_suit = perspective.get_trump_suit()
        # print(moves)

        highest_move = None
        highest_score = 0
        highest_trump_score = 0
        highest_trump_move = None

        for move in moves:
            # first check if we can do a trump exchange
            if move.is_trump_exchange():
                return move

            # then check if we have a marriage
            if move.is_marriage():
                return move
        
            score_of_card = scorer.rank_to_points(move.cards[0].rank)
                
            # then check if we have a trump card
            if move.cards[0].suit == trump_suit and score_of_card > highest_trump_score:
                highest_trump_move = move

            # else play the highest card in our hand
            if score_of_card > highest_score:
                highest_score = score_of_card
                highest_move = move

        # print(highest_trump_move, ', ', highest_move)

        # if we have a trump move, play it
        if highest_trump_move != None:
            return highest_trump_move
        
        # else play the highest card there is in our hand.
        return highest_move


    def follow_suit(self, perspective: PlayerPerspective, leader_move: Move | None) -> Move:
        """
        If we do not have the first move, it should follow the suit if it can,
        otherwise it should play the lowest card.
        """
        scorer = SchnapsenTrickScorer()
        moves = perspective.valid_moves()
        trump_suit = perspective.get_trump_suit()
        # print(moves)

        highest_move = None
        highest_score = 0

        # if we have a move that can win the trick, play it
        for move in moves:
            score_of_card = scorer.rank_to_points(move.cards[0].rank)

            if move.cards[0].suit == leader_move.cards[0].suit:
                if score_of_card > scorer.rank_to_points(leader_move.cards[0].rank) and score_of_card > highest_score:
                    highest_score = score_of_card
                    highest_move = move

        if highest_move != None:
            # print(highest_move)
            return highest_move
        
        # if it cannot win the move, play the lowest card
        lowest_score = 12
        lowest_move = None
        for move in moves:
            score_of_card = scorer.rank_to_points(move.cards[0].rank)
            if score_of_card < lowest_score and move.cards[0].suit != trump_suit:
                lowest_score = score_of_card
                lowest_move = move
        
        # in the special case that we only have trump cards in hand, play the first available move
        if lowest_move == None:
            lowest_move = moves[0]

        # print(lowest_move)
        return lowest_move


