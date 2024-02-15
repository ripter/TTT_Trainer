# Implementing and Training a LoRA Model for TicTacToe: Learning Strategies and Outcomes.

The goal is to create a LoRA that can play a game of TicTacToe and learn along the way.


# Phase One

Each turn is represented as a text grid with text to indicate who should place the next mark.

```
 Next Play: X 
   |   |   
   |   |   
   |   | 
```
   
I generated a dataset comprising 25 game logs for training purposes, created through simulations where a human player competed against an algorithm placing marks randomly on the gameboard. In these simulations, the 'X' player secured victories in 24 games, while the 'O' player won a single game, with no instances of ties. These game logs were aggregated into a unified file named `all.jsonl`. Subsequently, this file was partitioned according to a distribution recommended by HuggingFace: 70% of the data was allocated to `train.jsonl` for training, 15% to `valid.jsonl` for validation, and the remaining 15% to `test.jsonl` for testing purposes. Following this data preparation, I conducted a series of 600 iterations of LoRA training on the Mistral-7B-v0.1 base model.

```
python -m mlx_lm.lora \                                                                                                                                                                                    
              --model models/Mistral-7B-v0.1/ \
              --train \
              --data data/ \
              --iters 600
```


The integration of LoRA significantly improves the model's capability to conform to the prescribed game format, marking a significant advancement over the baseline performance observed in the untrained Mistral-7B and previous iterations of ChatGPT, including versions 3.5 and 4. While the untrained Mistral model exhibited challenges in adhering to the game's format, and ChatGPT was only able to maintain format compliance momentarily, LoRA enables the model to consistently follow the game format throughout its duration.

The augmented model, with the inclusion of LoRA, experiences challenges when the player does not aim for a victory. When the player attempts to force a draw or seeks a loss, the AI's response mechanism is compromised, often incorrectly placing an 'X' in lieu of an 'O'. This error unintentionally tips the balance in favor of the 'X' player achieving victory.

To ensure a comprehensive gaming experience with the model, a `GameState` class has been developed. It is tasked with tracking the current player's turn, the configuration of the gameboard, and presenting the game state as a string representation accurately. However, this class does not possess the functionality to autonomously interpret the model's responses. As a result, it requires direct input from the user to update the AI's moves. This interaction is facilitated by displaying the machine learning (ML) model's response to the user and inquiring where the ML model has placed a mark.


