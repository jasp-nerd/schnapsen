from schnapsen.game import SchnapsenGamePlayEngine
from schnapsen.bots import RandBot
from schnapsen.bots import RdeepBot
from schnapsen.bots import LaidBackBot
from schnapsen.bots import RiskTakingBot
import random

random.seed(122)

engine = SchnapsenGamePlayEngine()

myrepeats = 10

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

total_win = []

print("Playing {} games:".format(int(totalgames)))
for a, b in matches:
    amount_win = {}
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

        if amount_win == {}:
            amount_win = {str(bots[p[0]]): 0, str(bots[p[1]]): 0}

        amount_win[str(winner_id)] += game_points

    total_win.append(amount_win)

print(total_win)


