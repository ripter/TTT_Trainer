import mlx.core as mx
from mlx.utils import tree_unflatten
from libs.mamba.mlx.mamba_lm_mlx import MambaLM, MambaLMConfig

# We need to get the model. The existing MambaLM.from_pretrained does not support local file paths
# So Let's do all the stuff it was going to do!
# model = MambaLM.from_pretrained(model_path)
def load_from_file(path):
    # Create the Model.
    # copied from: https://huggingface.co/state-spaces/mamba-130m/blob/main/config.json
    model_config = MambaLMConfig(d_model=768, n_layers=24, vocab_size=50277)
    model = MambaLM(model_config)
    
    # Copy the weights from the file into the model
    model.update(tree_unflatten(list(mx.load(path).items())))

    return model
