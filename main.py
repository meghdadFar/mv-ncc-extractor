from scipy.stats import norm
from IO import read_score, read_scores
from util import element_wise, filter_ncs
import scipy
from functions import to_gaussian, normalize
from gensim.models.keyedvectors import KeyedVectors
from distribution import calculate_score
import numpy as np
import logging
import sys
import configparser
import logging_config


if __name__ == '__main__':

    logging.info("Reading configuration from " + sys.argv[1])
    config = configparser.ConfigParser()
    config.read(sys.argv[1])

    logging.info('reading scores')
    reg, additive, sdmas, pmis, npmis = read_scores(config['PATH']['SCORES'])
    logging.info('reading evaluation')
    eval = read_score(config['PATH']['EVAL_SCORE'])

    # logging.info(('reading gensim model')
    # gensim_w2v_model = KeyedVectors.load_word2vec_format(config['PATH']['GENSIM'], binary=False)
    # eval = filter_ncs(eval, gensim_w2v_model)

    all_in_one_file = open(config['PATH']['OUTPUT']+'alltogether.csv', 'w')
    all_in_one_file.write('compound,human_rev,sdmas,pmi,npmi,reg_error\n')

    eval_list = []
    sdmas_list = []
    pmis_list = []
    npmis_list = []
    additive_list = []
    reg_list = []
    i = 0

    logging.info('filtering ncs, retrieving scores')
    for k in eval:
        eval_list.append(float(eval[k]))
        sdmas_list.append(float(sdmas[k]))
        pmis_list.append(float(pmis[k]))
        npmis_list.append(float(npmis[k]))
        additive_list.append(float(additive[k]))
        reg_list.append(float(reg[k]))
        all_in_one_file.write(k +
                              ',' + str(float(eval[k])) +
                              ',' + str(float(sdmas[k])) +
                              ',' + str(float(pmis[k])) +
                              ',' + str(float(npmis[k])) +
                              ',' + str(float(reg[k])) + '\n')
    all_in_one_file.flush()
    all_in_one_file.close()

    reg_norm = to_gaussian(reg_list)
    sdmas_norm = to_gaussian(sdmas_list)
    pmis_norm = to_gaussian(pmis_list)
    npmis_norm = to_gaussian(npmis_list)
    additive_norm = to_gaussian(additive_list)

    mult = element_wise(reg_list, additive_list)

    multivar_dist = calculate_score(reg_norm, additive_norm, smooth=True)


    def precision_at(reference_scores, scores, threshold, k):
        desc_scores_indices = sorted(range(len(scores)), key=lambda k: scores[k], reverse=True)
        reference_scores = np.asarray(reference_scores)
        greater_references = reference_scores > threshold
        greater_references = greater_references.astype(int) # boolean to 0, 1
        greater_references = greater_references.tolist()
        p_at = 0
        for i in range(0, k):
            index = desc_scores_indices[i]
            if greater_references[index] == 1:
                p_at += 1
        return p_at

    logging.info('Number of eval elements: ', str(len(eval_list)))

    print('----------------------------------------------------------------------------------------')
    print('Spearman rho bet. human score and additive score ', scipy.stats.spearmanr(additive_list, eval_list))
    print('Spearman rho bet. human score and reg score ', scipy.stats.spearmanr(reg_list, eval_list))
    print('----------------------------------------------------------------------------------------')
    print('Spearman rho bet. human score and SDMA', scipy.stats.spearmanr(normalize(sdmas_list), eval_list))
    print('Spearman rho bet. human score and NPMI', scipy.stats.spearmanr(normalize(npmis_list), eval_list))
    print('Spearman rho bet. human score and PMI', scipy.stats.spearmanr(normalize(pmis_list), eval_list))
    print('----------------------------------------------------------------------------------------')
    print('Spearman rho bet. human score and mult score ', scipy.stats.spearmanr(normalize(mult), eval_list))
    print('Spearman rho bet. human score and mult-dist score ', scipy.stats.spearmanr(normalize(multivar_dist), eval_list))
    print('----------------------------------------------------------------------------------------')
    k = 50
    threshold = 0.6
    print(' p_at reg',  precision_at(eval_list, reg_list, threshold=threshold, k=k))
    print(' p_at add',  precision_at(eval_list, additive_list, threshold=threshold, k=k))
    print(' p_at mult',  precision_at(eval_list, mult, threshold=threshold, k=k))
    print(' p_at multivar',  precision_at(eval_list, multivar_dist, threshold=threshold, k=k))

    # plot.hist(additive_norm, bins=10, color='r')
    # plot.show()
