import numpy as np
from gensim.models import KeyedVectors
import itertools as it
import logging
from multiprocessing import Pool
from scipy.stats import percentileofscore

logger = logging.getLogger(__name__)


class Tissue(object):
    """
    Tissue class
    """
    def __init__(
        self, 
        get_background=False, 
        number_background_words=10_000, 
        loggerLevel=logging.INFO,
        biggim_tissues=None,
        w2v_model_path=None
    ):
        """
        Constructor
        :param get_background:
        :param number_background_words:
        :param loggerLevel:
        :param biggim_tissues:
        :param w2v_model_path:
        """

        logger.setLevel(loggerLevel)
        logger.info("Loading biggim tissues...")

        with open(biggim_tissues, 'r') as f:
            self.tissues = [i.strip() for i in f.readlines()]

        logger.info("Loading w2v model...")

        self.wv_from_bin = KeyedVectors.load_word2vec_format(
            w2v_model_path,
            binary=True
        )
        
        self.tissues_map = {t: self.return_combinations(t) for t in self.tissues}

        logger.info("Loading done!")


    def get_distance(self, word, n=10, compare_with_background=False):
        """
        Uh gets distance?

        :param word:
        :param n:
        :param compare_with_background:
        :return:
        """
        word_array = self.return_combinations(word, return_checks=True)
        word_array, checks = zip(*word_array)
        
        skipped_words = [i for i,j in zip(word_array, checks) if not j]
        
        if skipped_words: 
            logger.warning("Skipped words: %s" % ','.join(skipped_words))
        
        word_array = [i for i, j in zip(word_array, checks) if j]
        
        out = np.vstack([self.single_word_distance(w) for w in word_array])
        out = np.mean(out, axis=0)

        if compare_with_background:
            out = [(self.tissues[ind], j, percentileofscore(i,j)) \
                for ind, (i,j) in enumerate(zip(self.background, out))]

            out = sorted(out, key=lambda x:x[1], reverse=True)[:n]

            return out

        out = sorted(zip(self.tissues, out), key=lambda x:x[1], reverse=True)[:n]
        
        return out


    def single_word_distance(self, word): 
        storage = []
        for t in self.tissues: 
            a = self.wv_from_bin[word]
            b = np.vstack([self.wv_from_bin[k] \
                for k in self.tissues_map[t] if k in self.wv_from_bin.vocab])
            
            out = self.wv_from_bin.cosine_similarities(a,b)
            
            storage.append(np.mean(out))
            
        return np.array(storage)


    def calculate_background(self, n): 
        self.random_words = np.random.choice(list(self.wv_from_bin.vocab.keys()), 10_000)
        
        self.background = [self.single_word_distance(word) for word in self.random_words]
        self.background = np.array(self.background)


    def return_combinations(self, word, return_checks=False):
        """TODO: Return in_vocab"""
        
        array = word.split('_')

        for i in range(len(array)):
            #combinations contain all possible permutations
            combinations = self.consecutive_combinations(array, i+1)
            
            # combination is one of the permutation
            for combination in combinations: 
                in_vocab = []
                for vocab in combination: 
                    in_vocab.append(vocab in self.wv_from_bin.vocab)

                if all(in_vocab):
                    if return_checks: 
                        return list(zip(combination, in_vocab))
                    
                    return combination
            
        if return_checks: 
            return list(zip(combination, in_vocab))

        return combination


    def consecutive_combinations(self, array, cuts): 
        """Enumerate all possible combination in order with a certain number of breaks"""
        
        length = len(array)
        if cuts < 1 or cuts > length: 
            raise ValueError("Number of cuts must be between 1 and the length of the array")
        
        storage = []
        for inds in it.combinations(range(length), cuts): 
            if inds[0] != 0: 
                continue 
                
            intermediate = []
            for i in range(len(inds) - 1): 
                element = '-'.join(array[inds[i]: inds[i+1]])
                intermediate.append(element)
            
            element = '-'.join(array[inds[-1]:])
            intermediate.append(element)
                
            storage.append(intermediate)
            
        return storage