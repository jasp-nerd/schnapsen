from schnapsen.game import Bot, Move, PlayerPerspective
from schnapsen.game import SchnapsenTrickScorer
from schnapsen.deck import Card, Suit, Rank


class RiskTakingBot(Bot):
    def get_move(self, perspective: PlayerPerspective, leader_move: Move | None) -> Move:
        """
        Schnapsen bot, with a risk taking strategy.
        Playing the high cards first in order to win the game as quick as possible.
        """

        return self.condition1(perspective, leader_move)

    def condition1(self, perspective: PlayerPerspective, leader_move: Move | None) -> bool:
        moves = perspective.valid_moves()
        trump_suit = perspective.get_trump_suit()

        return moves[0]
