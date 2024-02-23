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

That creates the file `adapters.npz`.  (If you change the adapters filename, you can specifiy the new name with the `--adapter-file` argument.)

To test the new LoRA, we can use the same `mlx_lm.lora` script, but instead of `--train` we pass in `--prompt`.

```
python -m mlx_lm.lora \                                                                                                                                                                                 
                    --model models/Mistral-7B-v0.1/ \
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

The results it generates *mostly* contains the part we require for the UI. "Last Play: O, 3". If the number of tokens it generates it too high, it will try to play again. Right now, I'm using a max tokens of 35 and that works well. Sometimes random characters appears in the response, or the gameboard is missing position 8. But those can be ignored by the UI.

This is a significant improvement over the base model.

* Base Model
	* 0/ Entire response is correct. 
	* 0/ Contains a correct "Last Play:" but has other bad data.
	* 2/ Had "Last Play:" but picked an invalid move.
	* 0/ Llama Spit! (Aka nothing is correct)
* With LoRA 
	* 7/20 Entire response is correct. 
	* 13/20 Contains a correct "Last Play:" but has other bad data.


#### Fusing the model

There is not a lot of support for text models running with a LoRA. (Although it is extrememly common for the image generation models.) So we need to create a new model the combines the base with our LoRA.

```
python -m mlx_lm.fuse \                                                                                                                                                                               
                    --model models/Mistral-7B-v0.1/
```

This creates our fused model at `lora_fused_model` by default.  So let's test this new model and see if we get the LoRA improvements.

```
python -m mlx_lm.generate \                                                                                                                                                                            
                    --model lora_fused_model/ \
                    --max-tokens 35 \
                    --seed (printf "%d" '0x'(openssl rand -hex 4)) \
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


* Fused Model
	* 0/20 Entire response is correct. 
	* 20/20 Contains a correct "Last Play:" but has other bad data.
	* 0/20 Llama Spit! (Aka nothing is correct)

I don't know why this provides different results than the Base + LoRA version, but it does.