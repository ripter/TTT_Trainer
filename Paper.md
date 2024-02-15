# Implementing and Training a LoRA Model for TicTacToe: Learning Strategies and Outcomes.

The goal is to create a LoRA that can play a game of TicTacToe and learn along the way.

**Inverting Control Dynamics in Tic-Tac-Toe Gameplay with AI Models.** When initiating a game of Tic-Tac-Toe, wherein the model, such as ChatGPT, is invited to play, it typically performs admirably, engaging by placing marks based on the player's input. Despite its competence, the model encounters challenges in longer games, revealing limitations in its gameplay strategy. A significant limitation arises from the model's dual role as both the game's moderator and its arbiter of truth. Consequently, the player's interaction is confined to the structured input recognized by the model, limiting the gameplay experience. To address this, one of our training objectives is to invert this control mechanism. By introducing a third-party entity, specifically a Python class, we shift the responsibility of maintaining the game's state and truth. This entity oversees the game's progression, arbitrating both players' moves and determining the conclusion of the game. Such an approach democratizes the gameplay, placing the machine learning model and the human player on equal footing, thereby enriching the interactive experience and allowing for a more dynamic and flexible game structure.

[Image of ChatGPT Failing to play TTT](./meda/ChatGPT TTT Game.png)





## Phase One

The current game state is depicted using a text-based grid, complemented by a tag that specifies which player's turn it is next. This setup is designed to emulate the experience of two individuals playing TicTacToe remotely, mirroring the traditional long-distance correspondence games. Each player takes turns marking their chosen cell on the grid, representing either an 'X' or an 'O', and then sends the updated grid to their opponent. The simplicity of this approach facilitates an intuitive and accessible gaming experience. For example, when it's 'X's turn to play, the game board might appear as follows, waiting for 'X' to make a move:

```
 Next Play: X 
   |   |   
   |   |   
   |   | 
```
This method ensures that both players are continuously informed of the game's progress and can strategize their next move accordingly, maintaining the interactive essence of TicTacToe.

The GameState class is designed to maintain the current state of the TicTacToe game, including tracking the active player, the gameboard layout, and representing these elements as a string. However, it lacks the capability to independently parse and apply the machine learning model's moves. Consequently, manual input from the user is required to update the AI's actions based on its responses, necessitating a direct query to the user regarding the placement of the AI's mark.


### Training

I generated a dataset comprising 25 game logs for training purposes, created through simulations where a human player competed against an algorithm placing marks randomly on the gameboard. In these simulations, the 'X' player secured victories in 24 games, while the 'O' player won a single game, with no instances of ties. These game logs were aggregated into a unified file named `all.jsonl`. Subsequently, this file was partitioned according to a distribution recommended by HuggingFace: 70% of the data was allocated to `train.jsonl` for training, 15% to `valid.jsonl` for validation, and the remaining 15% to `test.jsonl` for testing purposes. Following this data preparation, I conducted a series of 600 iterations of LoRA training on the Mistral-7B-v0.1 base model.

```
python -m mlx_lm.lora \                                                                                                                                                                                    
              --model models/Mistral-7B-v0.1/ \
              --train \
              --data data/ \
              --iters 600
```


### Results

The integration of LoRA significantly improves the model's capability to conform to the prescribed game format, marking a significant advancement over the baseline performance observed in the untrained Mistral-7B and previous iterations of ChatGPT, including versions 3.5 and 4. While the untrained Mistral model exhibited challenges in adhering to the game's format, and ChatGPT was only able to maintain format compliance momentarily, LoRA enables the model to consistently follow the game format throughout its duration.

The augmented model, with the inclusion of LoRA, experiences challenges when the player does not aim for a victory. When the player attempts to force a draw or seeks a loss, the AI's response mechanism is compromised, often incorrectly placing an 'X' in lieu of an 'O'. This error unintentionally tips the balance in favor of the 'X' player achieving victory.



## Phase 2: Enhancing GameState and ML Model Interaction

At this juncture, I'm confronted with a pivotal choice: delve into quantifying the data needed for the model to proficiently play TicTacToe, or refine the prompt structure to enable the GameState class to autonomously interpret the ML model's responses, thus eliminating the need for manual intervention. My decision branches into exploring both avenues, albeit with a primary emphasis on refining the interaction between the GameState mechanism and the ML model.

The initial step in this process involves revisiting the prompt format. Currently, the GameState encapsulates two essential pieces of information: which player's turn it is and the visual representation of the gameboard. To facilitate a more intuitive understanding by the GameState of the ML's responses, an additional datum is introduced: the position where the last player placed their mark. This modification will allow the GameState to read the ML's move, and validate that the move is valid.

```
Last Play: X, 4
Next Play: O 
  O |   |   
  X | X  |   
   |   | 
```

To support this new format, the GameState class will need to be able to read back the string representation it generates. It needs to pull state from the first two lines and then compare it's internal board state with the string version provided.




