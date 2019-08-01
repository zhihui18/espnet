import os

import sentencepiece as spm


root = os.path.dirname(os.path.abspath(__file__))


def test_spm_compatibility():
    """"test python API with legacy C++ tool outputs

    NOTE: hard-coded strings are generated by spm v0.1.82
    """
    testfile = root + "/tedlium2.txt"
    nbpe = 100
    bpemode = "unigram"
    bpemodel = "test_spm"

    # test train
    spm.SentencePieceTrainer.Train(
        f"--input={testfile} --vocab_size={nbpe} --model_type={bpemode} \
          --model_prefix={bpemodel} --input_sentence_size=100000000")
    with open(f"{bpemodel}.vocab", "r") as fa, \
            open(root + "/tedlium2.vocab", "r") as fb:
        for a, b in zip(fa, fb):
            assert a == b

    # test encode and decode
    sp = spm.SentencePieceProcessor()
    sp.Load(f"{bpemodel}.model")
    txt = "test sentencepiece."
    actual = sp.EncodeAsPieces(txt)
    expect = "▁ te s t ▁ s en t en c e p ie c e .".split()
    assert actual == expect
    assert sp.DecodePieces(actual) == txt
