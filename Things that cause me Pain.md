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



## The mistake of llama.cpp

I had forgottent that llama.cpp runs everything on the CPU. It's never going to take full advantage of my hardware. I shouldn't even be using it anymore. Once I built a basic server using the mlx's `load` and `generate` functions, I got the server working and it generates results significantly faster than llama.cpp did.

---

Converting the fused model into a GGUF has been, challenging. The current versions (mlx==0.2.0, mlx-lm==0.0.13) appears to break something with the tokenizer files. In order to have llama.cpp's convert load the model. I replaced the tokenizer.* files in th lora_fused with the ones from the base model. This allowed llama.cpp to create the gguf file.

nope, that didn't work. While it created the file, the modle gets stuck in and endless loop and never responds.


**What Have I learned so far?**

* Llama.cpp script errors when trying to convert a fused model to GGUF
* Llama.cpp script works when trying to convert the base model.
* If I copy the base model’s token files to the fuse model. The script works, but the model does not run properly.
* The ‘save_gguf’ function from mlx doesn’t do much. It writes a list of arrays to a file with the GGUF extension. That’s it. Barely more than a native file write.
* mlx library’s test for save_gguf only tests that it was able to write a 4x4 array of 1s to disk.
* I searched GitHub. The only examples of using save_gguf all come from that test file. No one I’ve been able to talk to so far has used the function

**Options**

* I could try to quantize the fused model, then see if the llama.cpp convert script can handle that.
* I can read up on the GGUF format and figure out how to save it in the right format.
* Dig into llama.cpp’s convert script and see why it’s erroring. Use that to figure out a fix.


I'm going to learn more about the GGUF format and see if I can fix my export script!

**Head Desk**

So I realise I've been chasing a problem I don't really have. I've been so focused on Llama.cpp because that is what I used on my really old hardware. That tool does everything in the CPU! I want to use my GPU! So even if I get the fuse model converted properly to a GGUF, I'll still be running thing on the CPU. In order to take full advantage of my hardware, I need to take the example server provided by MLX, and turn it into something I can use for this project. I did a google search to see if someone else did that already, but alias MLX is still very very new.

