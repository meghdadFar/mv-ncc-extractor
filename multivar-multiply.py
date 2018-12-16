import scipy
from IO import read_sdma, read_pmi, read_score, reddy_ncs
from util import element_wise


if __name__ == '__main__':

    sdmas = read_sdma('/Users/svm/Resources/non-comp/ncs/reddy_sdma2.txt')
    pmis, npmis = read_pmi('/Users/svm/Resources/non-comp/ncs/_pmi_npmi.txt')
    additive = read_score('/Users/svm/Resources/non-comp/scores/additive_scores.txt')
    reg = read_score('/Users/svm/Resources/non-comp/scores/reg_scores.txt')

    eval_ncs, eval_scores = reddy_ncs('/Users/svm//Resources/non-comp/ncs/MeanAndDeviations.clean.txt')


    sdmas_list = []
    pmis_list = []
    npmis_list = []
    additive_list = []
    reg_list = []


    for k in eval_ncs:
        sdmas_list.append(float(sdmas[k]))
        pmis_list.append(float(pmis[k]))
        npmis_list.append(float(npmis[k]))
        additive_list.append(float(additive[k]))
        reg_list.append(float(reg[k]))


    print 'Spearman rho bet. human score and additive score ', scipy.stats.spearmanr(additive_list, eval_scores)
    print 'Spearman rho bet. human score and reg score ', scipy.stats.spearmanr(reg_list, eval_scores)
    mult = element_wise(reg_list, sdmas_list, npmis_list)
    print 'Spearman rho bet. human score and mult score ', scipy.stats.spearmanr(mult, eval_scores)





