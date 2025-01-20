from schnapsen.game import SchnapsenGamePlayEngine
from schnapsen.bots import RandBot
from schnapsen.bots import RdeepBot
from schnapsen.bots import LaidBackBot
from schnapsen.bots import RiskTakingBot
import random

random.seed(122)

engine = SchnapsenGamePlayEngine()

myrepeats = 100

# Create bots
bot1 = LaidBackBot(name="LaidBackBot")
bot2 = RiskTakingBot(name="RiskTakingBot")
bot3 = RandBot(rand=random.Random(42), name="RandBot")
bot4 = RdeepBot(num_samples=10, depth=10, rand=random.Random(455), name="RdeepBot")

# remove or add the bots you want to this list

bots = [bot1, bot2, bot3, bot4]
n = len(bots)
wins = {str(bot): 0 for bot in bots}
matches = [(p1, p2) for p1 in range(n) for p2 in range(n) if p1 < p2]

totalgames = (n * n - n) / 2 * myrepeats
playedgames = 0

total_win_score = []
total_win_games = []

print("Playing {} games:".format(int(totalgames)))
for a, b in matches:
    amount_win_score = {}
    amount_win_games = {}
    for r in range(myrepeats):
        if random.choice([True, False]):
            p = [a, b]
        else:
            p = [b, a]

        winner_id, game_points, score = engine.play_game(
            bots[p[0]], bots[p[1]], random.Random(45)
        )

        wins[str(winner_id)] += game_points

        playedgames += 1
        print(
            "Played {} out of {:.0f} games ({:.0f}%): {} \r".format(
                playedgames, totalgames, playedgames / float(totalgames) * 100, wins
            ),
        )

        if amount_win_score == {}:
            amount_win_score = {str(bots[p[0]]): 0, str(bots[p[1]]): 0}
        if amount_win_games == {}:
            amount_win_games = {str(bots[p[0]]): 0, str(bots[p[1]]): 0}

        amount_win_score[str(winner_id)] += game_points
        amount_win_games[str(winner_id)] += 1

    total_win_score.append(amount_win_score)
    total_win_games.append(amount_win_games)

print('Total Score: \n', total_win_score)
print('----------------------')
print('Games Won: \n', total_win_games)


