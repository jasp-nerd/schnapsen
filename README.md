# Schnapsen Bot Strategy Analysis  

## About This Project  
This project measures risk-taking vs. laid-back strategies in the card game Schnapsen. We extended the [Schnapsen framework](https://github.com/intelligent-systems-course/schnapsen) by adding two rule-based bots and benchmarking their performance.  

## What We Added  
1. **RiskTakingBot (Aggressive Strategy)**  
   - Prioritizes high-value cards, trump exchanges, and marriages early.  
   - Always attempts to win tricks when possible.  
   - Location: `src/schnapsen/bots/aggressive.py`  

2. **LaidBackBot (Passive Strategy)**  
   - Conserves high-value cards for later phases.  
   - Minimizes point loss by playing low-value cards first.  
   - Uses trump cards only when necessary.  
   - Location: `src/schnapsen/bots/passive.py`  

## How to Run  
1. **Bot Tournament**:  
   Execute `bot_comparison.py` to run matches between bots:  
   ```bash  
   python executables/bot_comparison.py  
   ```  
   This script runs 1,000 games between:  
   - `LaidBackBot`  
   - `RiskTakingBot`  
   - `RandBot` 
   - `RdeepBot`   

   Results (win rates and scores) are printed to the console.  

2. **Reproducibility**:  
   - A fixed random seed (`seed=155`) ensures reproducible outcomes.  
   - Adjust `myrepeats` in `bot_comparison.py` to change the number of games.  

## Customization  
- **Add/Remove Bots**: Modify the `bots` list in `bot_comparison.py`:  
  ```python  
  bots = [bot1, bot2, bot3, bot4]  # Add/remove bots here  
  ```  
