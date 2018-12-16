import re


def read_pmi(file_path):
    pmis = {}
    npmis = {}
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()
        for l in lines:
            elements = l.split(" ")
            nc = elements[0] + " " + elements[1]
            pmis[nc] = elements[2]
            npmis[nc] = elements[3]
    return pmis, npmis


def read_sdma(file_path):
    sdmas = {}
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()
        for l in lines:
            elements = l.split(" ")
            nc = elements[0] + " " + elements[1]
            sdmas[nc] = elements[2]
    return sdmas


def read_score(file_path):
    scores = {}
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()
        for l in lines:
            elements = l.split('\t')
            nc = elements[0]
            scores[nc] = elements[1]
    return scores


def reddy_ncs(file_path):
    ncs = []
    scores = []
    nc_to_score = {}
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()
        for l in lines:
            # res = re.search('(\w+)-\w+\s(\w+)-\w+\s', l)
            res = re.match('(\w+)-\w+\s(\w+)-\w+\t([\s0-9.]+)$', l)
            if res:
                nc = res.group(1) + ' ' + res.group(2)
                ncs.append(nc)
                scores.append(float(res.group(3).split(" ")[4]))
                nc_to_score[nc] = float(res.group(3).split(" ")[4])
    return ncs, scores, nc_to_score


def read_scores(path):
    sdmas = read_score(path+'_sdma.csv')
    pmis = read_score(path+'_pmi.csv')
    npmis = read_score(path+'_npmi.csv')
    additive = read_score(path+'additive_scores.csv')
    reg = read_score(path+'reg_scores.csv')
    return reg, additive, sdmas, pmis, npmis
