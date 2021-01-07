from vietocr.tool.translate import build_model, translate, process_input
from tools.utils import download_model
import torch
import os


class Reader:
    def __init__(self, config):
        device = config['device']
        model, vocab = build_model(config)
        weights = config['weights']
        #
        if not os.path.exists(weights):
            download_model("reader")
        model.load_state_dict(torch.load(weights, map_location=torch.device(device)))
        #
        self.config = config
        self.model = model
        self.vocab = vocab

    def predict(self, img):
        img = process_input(img, self.config['dataset']['image_height'],
                            self.config['dataset']['image_min_width'],
                            self.config['dataset']['image_max_width'])

        img = img.to(self.config['device'])
        #
        s, _ = translate(img, self.model)
        s = s[0].tolist()
        s = self.vocab.decode(s)
        return s
