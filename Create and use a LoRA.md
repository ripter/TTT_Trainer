# Create and use a LoRA


To start we need two things, the training data and the base model.

* data/
	* game_log1.txt
	* game_log2.txt
	* etc...
* model/
	* Mistral-7B-v0.1/
		* config, safetensorts, tokenizer, etc


Make sure you setup and use a virtual environment with working with python.

```
# Create the venv
python3 -m venv venv

# Start the venv
source venv/bin/activate
```



Convert the data/*.txt files into a single all.jsonl file.

```
python scripts/create_all_jsonl.py "*.txt"
```


Split the all.jsonl into train.jsonl, valid.jsonl, test.jsonl

```
# TODO: Add code here
``


Create the adaptor

```
python -m mlx_lm.lora \                                                                                                                                                                             
                         --model models/Mistral-7B-v0.1/ \
                         --data data/ \
                         --train
```

That creates the file `adapters.npz`. We can then test it using the same lora script.

```
python -m mlx_lm.lora \                                                                                                                                                                                 
                    --model models/Mistral-7B-v0.1/ \
                    --adapter-file adapters.npz \
                    --max-tokens 35 \
                    --prompt "3TBot is playing TicTacToe with User.
                3TBot is playing as O. User is playing as X.
                Only play when it is your turn.
                Update the gameboard with your move.
                Stop playing when someone wins.

                Next Play: X
                Last Play: None, None
                   |   |
                   |   |
                   |   |


                Next Play: O
                Last Play: X, 0
                 X |   |
                   |   |
                   |   |  "
```

The results it generates *mostly* contains the part we require for the UI. "Last Play: O, 3". If the number of tokens it generates it too high, it will try to play again. Right now, I'm using a max tokens of 35 and that works well. There is some random characters appears in the response as well. But those can be ignored by the UI.

Running the same command, but without the `--adapter-file adapters.npz \` allows us to compare the results with the LoRA and without. 

Using my human judgement for "Working" or not, here is a small smaple. We can see the LoRA give the correct response more often than the base model. While not captured here, it should be noted that most of the "bad data" in the LoRA version was because it missed a " | " at the end, or failed to place it's mark on the board. While the Base mode's "bad data" was mostly because it contained random text, characters, and other issues. This means that even the "bad" versions of the LoRA are closer to accurate than the base model's "bad" versions.

* No LoRA
	* 2/10 Entire response is correct. 
	* 7/10 Contains a correct "Last Play:" but has other bad data.
* With LoRA Phase 2
	* 5/10 Entire response is correct. 
	* 5/10 Contains a correct "Last Play:" but has other bad data.

