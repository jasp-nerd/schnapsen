# Schnapsen Game Bot Project

## About This Project
This is my school project where I added two new bots to play the card game Schnapsen. I forked this project from my teacher's original repository and added my own bot implementations.

## What I Added
1. **Aggressive Bot (RiskTakingBot)**
   - Takes more risks by playing high-value cards first
   - Always tries to win tricks when possible
   - Prioritizes trump cards and marriages
   - Location: `src/schnapsen/bots/aggresive.py`

2. **Passive Bot (LaidBackBot)**
   - Plays more carefully by using low-value cards first
   - Saves trump cards for when they're really needed
   - Only uses marriages when available
   - Location: `src/schnapsen/bots/passive.py`
