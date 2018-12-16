import argparse
import numpy as np
import gaussianize as g



def get_multivar_args():
    parser = argparse.ArgumentParser(description="Calculates the non-compositionality of the two words noun compounds "
                                                 "through multivariate distribution of different measurements "
                                                 "of non-compositionality.")

    parser.add_argument('-p2vw', '--path-to-word-vectors', help="Path to word vectors", dest='p2vw')
    parser.add_argument('-p2tc', '--path-to-train-compounds', help="Path to training compounds", dest='p2tc')
    parser.add_argument('-p2ec', '--path-to-eval-compounds', help="Path to evaluation compounds", dest='p2ec')
    parser.add_argument('-p2out', '--path-to-out-dir', help="Path to a directory for writing results", dest='p2out')
    args = parser.parse_args()
    return args


def to_gaussian(score_list):
    x = np.array(score_list)
    out = g.Gaussianize(strategy='brute')
    out.fit(x)
    y = out.transform(x)
    return y.flatten()


def has_vector(w, gensim_w2v_model):
    parts = w.split(' ')
    nc = parts[0]+'_'+parts[1]
    if nc in gensim_w2v_model.vocab:
        return True


def normalize(data):
    data = np.array(data)
    normalized_data = (data - np.min(data)) / (np.max(data) - min(data))
    return normalized_data
