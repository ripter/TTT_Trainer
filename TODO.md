# Interface

Play a TicTacToe game using a LLM interface.

✅ Play script that uses the model.
    ✅ Test in Notebook.
        ✅ Run full model in notebook.
        ✅ Run with `GameState` output.
    [ ] Test using llama.cpp's web interface.
        [ ] Model needs to be converted into gguf for llama.cpp
        
✅ Play script can log game to file.



# Training

✅ Use MLX library to create LoRA for model.
✅ Use LoRA when testing model.
[ ] Create data with bad user input.



## Round 1:

Training Data consists of game logs generated by a human player. The log format is enforced by the `GameState` object's to string method (`__str__`). It also includes the instruction message with hardcoded names. These logs only include valid and well formatted data.


