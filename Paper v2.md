# Paper v2

# Utilizing MLX for Enhanced TicTacToe Gameplay with Mistral 7B and LoRA

**Abstract:** The objective of this study is to harness the capabilities of the newly developed [MLX library by Apple](https://ml-explore.github.io/mlx/build/html/index.html) in training the Mistral 7B model, with an aim to play the game of TicTacToe. This research incorporates a graphical user interface (GUI) for interactive gameplay, leveraging the advancements in machine learning and user experience design.



### Setup the Environment

First thing we need to do is activate python's virtual environment and install the required packages. (If you encounter an error that `python` is unknown or it is the wrong version, make sure the virtual environment has been activated.)

```
source venv/bin/activate
python -m pip install -r requirements.txt
```

> (Fish users should use `source venv/bin/activate.fish` instead.)


### Download the model.

You can find the [Mistral 7B model on huggingface](https://huggingface.co/mistralai/Mistral-7B-v0.1) 

Download the model to the models folder so the result is `models/Mistral-7B-v0.1/` That folder should containe the `*.safetensors` along with `config.json`, and the tokenizer files.


### Start the UI

When starting the UI server, you need to pass in a model to use when generating a response. 

```
python webUI/server.py --model models/Mistral-7B-v0.1/
```

> run `python webUI/server.py -h` to see a full list of options, including running the model with a LoRA.


The UI will run on [localhost:4400](http://localhost:4400/index.html)

