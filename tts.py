import json
import os
import re
import sys
import librosa
import numpy as np
import torch
from torch import no_grad, LongTensor
import commons
import utils
import soundfile
from models import SynthesizerTrn
from text import text_to_sequence, _clean_text
from mel_processing import spectrogram_torch

limitation = os.getenv("SYSTEM") == "spaces"  # limit text and audio length in huggingface spaces


def get_text(text, hps, is_phoneme):
    text_norm = text_to_sequence(text, hps.symbols, [] if is_phoneme else hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = LongTensor(text_norm)
    return text_norm



def tts_fn(model, hps, speaker_ids, text, speaker, speed, is_phoneme):

    speaker_id = speaker_ids
    stn_tst = get_text(text, hps, is_phoneme)
    with no_grad():
        x_tst = stn_tst.unsqueeze(0)
        x_tst_lengths = LongTensor([stn_tst.size(0)])
        sid = LongTensor([speaker_id])
        audio = model.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=.667, noise_scale_w=0.8,
                                length_scale=1.1)[0][0, 0].data.cpu().float().numpy()
    del stn_tst, x_tst, x_tst_lengths, sid
    res_path = f'temp.ogg'
    soundfile.write(res_path, audio, 22050)
    print(sys.argv[1])
    return "Success", (22050, audio)



def create_to_phoneme_fn(hps):
    def to_phoneme_fn(text):
        return _clean_text(text, hps.data.text_cleaners) if text != "" else ""

    return to_phoneme_fn

if __name__ == '__main__':
    models_tts = []
    name = 'TTS'
    lang = '日本語'
    example = 'こんばんは'
    config_path = "model.json"
    model_path = "model.pth"
    hps = utils.get_hparams_from_file(config_path)
    model = SynthesizerTrn(
        len(hps.symbols),
        hps.data.filter_length // 2 + 1,
        hps.train.segment_size // hps.data.hop_length,
        n_speakers= 0, #hps.data.n_speakers,
        **hps.model)
    utils.load_checkpoint(model_path, model, None)
    model.eval()
    speaker_ids = [0]
    speakers = [name]

    t = 'vits'
    #models_tts.append((name, speakers, lang, example,
    #                    hps.symbols, create_tts_fn(model, hps, speaker_ids),
    #                    create_to_phoneme_fn(hps)))
    
    a = tts_fn(model, hps, speaker_ids, sys.argv[1], speakers[0], 1, False)
                                
