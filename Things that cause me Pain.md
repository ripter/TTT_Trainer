# Things that cause me Pain

## Using mlx_lm.generate

It appears to use the same seed if you do not specify one! I had expected it to use a random seed each time.

Using fish, I generate a random seed with 
```
--seed (printf "%d" (openssl rand -hex 4 | tr -d '\n'))
```


## Using mlx_lm.lora

So it appears that the `--adapter-file` flag is just if I want to use a file name other than the default. If you do no specify it, `--prompt` will still use the LoRA with the default name.

If you want to run the model *without* the LoRA, use `mlx_lm.generate` instead.

### removed from the paper, but part of this pain.

Running the same command, but without the `--adapter-file adapters.npz \` allows us to compare the results with the LoRA and without. 

Using my human judgement for "Working" or not, here is a small smaple. We can see the LoRA give the correct response more often than the base model. While not captured here, it should be noted that most of the "bad data" in the LoRA version was because it missed a " | " at the end, or failed to place it's mark on the board. While the Base mode's "bad data" was mostly because it contained random text, characters, and other issues. This means that even the "bad" versions of the LoRA are closer to accurate than the base model's "bad" versions.

* No LoRA
	* 2/10 Entire response is correct. 
	* 8/10 Contains a correct "Last Play:" but has other bad data.
* With LoRA Phase 2
	* 5/10 Entire response is correct. 
	* 5/10 Contains a correct "Last Play:" but has other bad data.



For a sanity check, let's use a different script to test the base model.

```
python -m mlx_lm.generate \                                                                                                                                                                            
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

* Base Model
	* 0/10 Entire response is correct. 
	* 0/10 Contains a correct "Last Play:" but has other bad data.
	* 10/10 Response is Llama Spit.


Something fishy is going on.  Why does the `generate` script produce garbage every time, but the `lora` script, without a lora specified, does an ok job? My first thought is that the `lora` script is still using the lora, even if I don't specify it? Easy to check.

```
git stash
rm adapters.npz
rm -rf checkpoints
```

now there are no LoRA files to find. Let's run the test again.


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

> ValueError: Adapter file adapters.npz missing. Use --train to learn and save the adapters.npz.

Ahhhhh, yeah. So my inital test is invalid. *sigh* that only took two days. So it appears that the `--adapter-file` flag is just if I want to use a file name other than the default. If you do no specify it, `--prompt` will still use a LoRA with the default name.



