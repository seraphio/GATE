import clip
import numpy as np
import pytest
import torch
from PIL import Image
from rich import print

# write your own version of this and have a tests that confirms that it predicts the
# same stuff
# perhaps write your own version and then train it and compare the results


@pytest.mark.parametrize("model_name", clip.available_models())
def test_consistency(model_name):
    device_idx = torch.cuda.current_device() if torch.cuda.is_available() else None
    device = "cpu" if device_idx is None else f"cuda:{device_idx}"
    py_model, transform = clip.load(model_name, device=device, jit=False)
    jit_model = py_model

    image = transform(Image.open("test_images/CLIP.png")).unsqueeze(0).to(device)
    text = clip.tokenize(["a diagram", "a dog", "a cat"]).to(device)

    with torch.no_grad():
        logits_per_image, _ = jit_model(image, text)
        jit_probs = logits_per_image.softmax(dim=-1).cpu().numpy()

        logits_per_image, _ = py_model(image, text)
        py_probs = logits_per_image.softmax(dim=-1).cpu().numpy()

    assert np.allclose(jit_probs, py_probs, atol=0.01, rtol=0.1)