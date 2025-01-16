from schnapsen.game import Bot, Move, PlayerPerspective
from schnapsen.game import SchnapsenTrickScorer
from schnapsen.deck import Card, Suit, Rank

class LaidBackBot(Bot):
    """
    Schnapsen bot with a laid back strategy.
    Playing the low cards first in order to minimize risk.
    """
    def get_move(self, perspective: PlayerPerspective, leader_move: Move | None) -> Move:
        
        # If we're in phase 2, delegate to a perfect information strategy
        # if perspective.get_phase() == GamePhase.TWO:
        #     return self.get_phase_two_move(perspective, leader_move)
        
        # Original phase 1 strategy
        if leader_move is None:
            return self.get_lowest_scoring_move(perspective, leader_move)
        else:
            return self.follow_suit(perspective, leader_move)
    
    def get_lowest_scoring_move(self, perspective: PlayerPerspective, leader_move: Move | None) -> Move:
        """
        If we have the first move, we should play moves with the lowest points:
        First check for marriages (as they score points), then non-trump low cards,
        and finally trump cards if necessary.
        """
        scorer = SchnapsenTrickScorer()
        moves = perspective.valid_moves()
        trump_suit = perspective.get_trump_suit()
        
        # first check if we can do a trump exchange
        for move in moves:
            if move.is_trump_exchange():
                return move
        
        # then check if we have a marriage
        for move in moves:
            if move.is_marriage():
                return move
        
        lowest_move = None
        lowest_score = float('inf')
        lowest_trump_move = None
        lowest_trump_score = float('inf')
        
        for move in moves:
            score = scorer.rank_to_points(move.cards[0].rank)
            
            # handle trump cards separately
            if move.cards[0].suit == trump_suit:
                if score < lowest_trump_score:
                    lowest_trump_score = score
                    lowest_trump_move = move
            else:
                if score < lowest_score:
                    lowest_score = score
                    lowest_move = move
        
        # never play trump cards when we have other options
        if lowest_move is not None:
            return lowest_move
        # only play trump as an absolute last resort when we have no other choice
        return lowest_trump_move
    
    def follow_suit(self, perspective: PlayerPerspective, leader_move: Move | None) -> Move:
        scorer = SchnapsenTrickScorer()
        moves = perspective.valid_moves()
        trump_suit = perspective.get_trump_suit()
        leader_card = leader_move.cards[0]
        leader_score = scorer.rank_to_points(leader_card.rank)
        
        def get_move_points(move: Move) -> int:
            return scorer.rank_to_points(move.cards[0].rank)
        
        # categorize our moves
        following_moves = [] # cards of the same suit
        non_trump_moves = [] # cards of other suits (excluding trump)
        trump_moves = [] # trump cards
        
        for move in moves:
            card = move.cards[0]
            if card.suit == leader_card.suit:
                following_moves.append(move)
            elif card.suit == trump_suit:
                trump_moves.append(move)
            else:
                non_trump_moves.append(move)
        
        # if we can follow suit
        if following_moves:
            # sort by top to bottom points
            following_moves.sort(key=get_move_points)
            
            # find moves that can win
            winning_moves = []
            for m in following_moves:
                if get_move_points(m) > leader_score:
                    winning_moves.append(m)
            
            if not winning_moves:
                # if we can't win, play our lowest card
                return following_moves[0]
            else:
                # if we must win, play the lowest winning card
                return winning_moves[0]
            
        # if we can't follow suit, prefer lowest non-trump card
        if non_trump_moves:
            lowest_move = non_trump_moves[0]
            lowest_points = get_move_points(lowest_move)
            for move in non_trump_moves[1:]:
                points = get_move_points(move)
                if points < lowest_points:
                    lowest_move = move
                    lowest_points = points
            return lowest_move
        
        # as a last resort, play lowest trump card
        if trump_moves:
            lowest_move = trump_moves[0]
            lowest_points = get_move_points(lowest_move)
            for move in trump_moves[1:]:
                points = get_move_points(move)
                if points < lowest_points:
                    lowest_move = move
                    lowest_points = points
            return lowest_move
        