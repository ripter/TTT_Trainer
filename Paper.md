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

In this phase, my objectives are twofold: firstly, to eliminate the requirement for human review of the ML model's responses, and secondly, to enhance the quality of the responses generated by the ML model for TicTacToe gameplay. These goals necessitate a dual approach: refining the data quantification for the ML model and improving the interaction framework between the GameState class and the ML model. The latter involves a critical reevaluation of the prompt structure, aiming to foster a more seamless and autonomous communication channel between the GameState mechanism and the ML model.

The refinement process begins with an overhaul of the current prompt format utilized by the GameState. This format, as it stands, provides essential information about whose turn it is and the current visual representation of the game board. To advance the GameState's autonomous interpretation of the ML model's responses, a significant enhancement is introduced: specifying the position of the last move made. This amendment is designed to empower the GameState with the capability to independently assess and validate the ML model's moves. Additionally, to improve user interaction and transparency, an optional error message feature has been developed to articulate the reasons behind any decisions not to alter the game state.

```
Next Play: O 
Last Play: X, 4 
   |   |   
   | X |   
   |   |   
Error message displayed here
```

To use this new prompt format, a function `convert_ai_response_to_move()` converts the prompt into a valid play for `GameState` or an error.



### Training Data

The initial dataset compilation strategy was deliberately unilateral, with 'X' configured to pursue victory aggressively, whereas 'O' was programmed to select moves randomly. This methodology aimed to expedite the generation of training data and establish a benchmark for subsequent phases. In contrast, the current dataset iteration simulates a scenario where a human competes against another human, meticulously capturing the essence of both participants striving for victory. A critical observation underpinning this approach is the inevitability of a tie in games played by two flawless TicTacToe players. To introduce variability and realistic game outcomes, the 'X' player was instructed to intentionally commit errors, thereby enabling 'O' to secure wins. Additionally, players were encouraged to forfeit in scenarios where the game's outcome became predictably unfavorable, adding another layer of strategic decision-making to the dataset.

For the creation of this diversified dataset, the `src/play_human_vs_human.py` script was deployed. This tool facilitated the simulation of authentic human-vs-human matches, ensuring a rich variety of game outcomes reflective of strategic missteps and conscious forfeitures.

The dataset now encompasses 24 meticulously curated game logs, realigned to capture a balanced spectrum of possible outcomes within TicTacToe matches:

  *  X Wins: 9 instances.
   * O Wins: 4 instances.
   * Tie: 7 instances.
   * Forfeit: 4 instances.




### Formatting the Data

After accumulating 24 game log files, the next critical step was to format them appropriately for the ML training process. The training script, specifically the `mlx_lm.lora` provided by Apple, necessitates the data to be organized into three distinct `.jsonl` files: `train.jsonl`, `valid.jsonl`, and `test.jsonl`. To facilitate this requirement, I developed a Python script dedicated to transforming the raw game logs into the expected format efficiently.

The transformation process was streamlined through the execution of two Python scripts:

1. **Build ALL.jsonl**

This script aggregates the game log files and formats them into a single `.jsonl` file.

```sh
python src/build_jsonl.py TTT_game_log  
```

2. **Split JSONL File:**

    Following the initial aggregation, this script divides the consolidated .jsonl file into three separate files (train, valid, and test) as per the training script's requirements.
    
```sh
python src/split_jsonl.py data/all_TTT_game_log.jsonl 
```

3. **Training with LoRA**

With the data correctly formatted, I proceeded to utilize the `mlx_lm.lora` script for training the model. The command below illustrates the training execution process:

```sh
python -m mlx_lm.lora \                                                                                                                                                                                    
              --model models/Mistral-7B-v0.1/ \
              --train \
              --data data/ \
              --iters 600
```

This training session, conducted on an Apple M3 Max with 128GB of RAM, required a substantial 92GB of RAM and concluded in just 44.92 minutes. The significant memory utilization underscores the computational rigor of the training process, while the training's completion time reflects an efficient use of resources, especially considering the complexity of the model involved. Notably, the model in its unquantized state demands approximately 18GB of RAM for operation, illustrating the high resource requirements intrinsic to running advanced ML models. 


### Testing the result

The final stage of our study involved rigorously testing the machine learning (ML) model to assess two critical aspects of its performance in TicTacToe gameplay: its ability to accurately update the "Last Play" line and its capacity to engage in a "fun" game from the player's perspective. "Fun" in this context implies a gameplay experience where the ML model presents a challenge but does not dominate, allowing for a balanced mix of wins and losses.

A series of ten games were conducted to evaluate the model's gameplay intelligence and strategic decision-making. The findings were as follows:

* **Game 1:** The ML overlooked a crucial opportunity to block the player, resulting in a missed defensive strategy.
* **Game 2:** While the ML successfully executed a block in the middle row, it inaccurately claimed to place a mark at position 8, leading to a discrepancy flagged as an AI failure.
* **Game 3:** The ML did not capitalize on a potential winning move along the first column.
* **Game 4:** Post a block by the player on the top row, the ML failed to prevent a winning move by the player on the last row.
* **Game 5:** The ML missed blocking the player's winning opportunity on the last row.
* **Game 6 & 7:** In both games, the player presented two winning positions, and the ML failed to block either, demonstrating a pattern of missed defensive strategies.
* **Game 8:** The ML neglected a winning move, inadvertently setting up the player for a win with two possible moves.
* **Game 9:** Despite successfully blocking a diagonal win, the ML failed to block a critical move on the last column.
* **Game 10:** The ML exhibited improved strategy by successfully blocking the player on three occasions: in the middle row, the middle column, and diagonally.
    
    
### Results

The testing phase demonstrated that the player could engage in multiple interactive games with the ML model. The model's updated interaction format significantly enhanced the user interface's (UI) capability to interpret the ML's responses and validate their accuracy. Although the ML model remains relatively easy to defeat, its performance in executing valid moves and engaging in the gameplay has notably improved. This advancement suggests a positive direction in the model's learning curve, indicating its potential for further refinement and sophistication in strategic gameplay.



## Phase 3: Improved UI & Spot Training

I created a webUI for the game that allows playing a model hosted by [llama.cpp's server](https://github.com/ggerganov/llama.cpp/tree/master/examples/server). The UI allows the user to play 


```
Next Play: O
Last Play: X, 4
   |   |   
 X | X |   
   |   |   

Next Play: X
Last Play: O, 5
   |   |   
 X | X | O 
   |   |   

// Emphasizes the importance of O blocking X's potential win on the middle row.
```


```
Next Play: X
Last Play: O, 3
   | O |   
   | X | X 
 O |   |   

Next Play: O
Last Play: X, 6
   | O |   
   | X | X 
 O | X |   

// Shows X taking a winning move on the bottom row, a lesson in recognizing and seizing win conditions.
```

```
Next Play: O
Last Play: X, 1
 X | X |   
   | O |   
   |   |   

Next Play: X
Last Play: O, 4
 X | X |   
   | O | O 
   |   |   

// O blocks X's attempt to win on the top row, learning from a past mistake where it failed to block a similar setup.
```

```
Next Play: X
Last Play: O, 4
 O |   |   
   | O |   
 X |   | X 

Next Play: O
Last Play: X, 5
 O |   |   
   | O | X 
 X |   | X 

// X blocks O's potential win on the diagonal, prioritizing defensive moves in critical situations.
```

```
Next Play: O
Last Play: X, 2
 X | X | O 
   | O |   
   |   |   

Next Play: X
Last Play: O, 6
 X | X | O 
   | O |   
   | O |   

// O blocks X's win on the top row and then goes on to block another potential win, showing adaptation to avoid repeating the same mistake.
```


```
Next Play: O
Last Play: X, 6
   |   | X 
   | X |   
 O |   |   

Next Play: X
Last Play: O, 3
   |   | X 
 O | X |   
 O |   |   

// Here, O blocks X's potential win on the right column, emphasizing the importance of immediate threat recognition and response.
```

```
Next Play: O
Last Play: X, 8
   | X |   
 O | O |   
   |   | X 

Next Play: X
Last Play: O, 6
   | X |   
 O | O | O 
   |   | X 

// Demonstrates O taking the winning move on the middle row, highlighting the importance of recognizing and seizing winning opportunities.
```

```
Next Play: O
Last Play: X, 2
 X |   | X 
   | O |   
   |   |   

Next Play: X
Last Play: O, 1
 X | O | X 
   | O |   
   |   |   

// O blocks one of X's potential wins, learning from a previous mistake where it failed to prevent a win in a similar setup.
```

```
Next Play: O
Last Play: X, 4
 X |   |   
   | X |   
   |   | O 

Next Play: X
Last Play: O, 7
 X |   |   
   | X |   
 O |   | O 

// O prioritizes blocking X's diagonal win while also setting up a potential win scenario for itself, showcasing strategic depth in play.
```

```
Next Play: O
Last Play: X, 5
   |   | O 
 X | O |   
   | X |   

Next Play: X
Last Play: O, 8
   |   | O 
 X | O | X 
   | X | O 

// O blocks a potential win by X on the bottom row and simultaneously prevents a diagonal win, demonstrating the ability to adapt and respond to multiple threats.
```







