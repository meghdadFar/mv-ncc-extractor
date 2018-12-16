import numpy as np
from scipy.stats import norm



def pdf(dist):
    mu, std = norm.fit(dist)
    p = norm.pdf(dist)
    p /= p.sum()
    return p, mu, std


def independent_prob(measurements):
    p, mu, std = pdf(measurements[0])
    res = p
    for m in measurements[1:-1]:
        p, _, _ = pdf(m)
        res = np.multiply(res, p)
    return res


def calculate_score(*args, **kwargs):
    scores = []
    smooth = kwargs.pop('smooth')
    nb_instances = len(args[0])
    for measurement in args:
        pp, mu, std = pdf(measurement)
        pp /= pp.sum()
        if smooth:
            measurement = np.log(1 + np.exp(measurement-mu))
        else:
            measurement = np.maximum((measurement-mu), 0)
        scores.append(measurement)
    res = np.ones(nb_instances)
    for s in scores:
        res = np.multiply(res, s)
    prob = independent_prob(args)
    res *= (1-np.array(prob))
    return res