from functions import has_vector
import matplotlib.pyplot as plot


def element_wise(*args):
    Z = []
    for i in range(0, len(args[0])):
        mult = 1
        for arg in args:
            mult *= arg[i]
        Z.append(mult)
    return Z


def filter_ncs(ncs_to_score, gensim_w2v_model):
    res = {}
    for nc in ncs_to_score:
        if not has_vector(nc, gensim_w2v_model):
            continue
        else:
            res[nc] = ncs_to_score[nc]
    return res


def showplot(s, bins=10, color='r'):
    plot.hist(s, bins=10, color='r')
    plot.show()