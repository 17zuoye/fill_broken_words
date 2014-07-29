# -*- coding: utf-8 -*-

from split_block import SplitBlock, SplitBlockGroup
from etl_utils import is_regular_word, regexp
from .utils import chars_len, ld
import math

class SentenceProcess(object):

    @classmethod
    def is_normal_sentence(cls, sentence, inspect=False):
        """ only check english words. """
        if inspect: print "[is_normal_sentence]", sentence

        for sb1 in SplitBlockGroup.extract(sentence):
            if inspect: print [sb1]

            #if ("Liu Xing" in sentence) and (sb1.string == 'it'): import pdb; pdb.set_trace()
            if sb1.is_letter and (not sb1.is_regular):
                # compact with name. e.g. is, am, of, ...
                if unicode(sb1.string) in ld.two_length_words: continue
                # compact with name. e.g. Liu Xing
                if sb1.p_sb and regexp.upper.match(sb1.string[0]): continue
                # compact with "(p,r,i,g,n,s)"
                if (sb1.p_sb and sb1.p_sb.is_other) and (sb1.n_sb and sb1.n_sb.is_other): continue

                # TODO remove am, is
                if sb1.string not in ['s', 'm', 'am', 'is']: return False
                # compact with plural. e.g. ["it is 5         s (英镑)", "pound"]
                if sb1.p_sb and sb1.p_sb.can_fill: continue
                # compact with I'm.
                if sb1.p_sb and sb1.p_sb.string == "'": continue
                # compact with " is "
                if (sb1.p_sb and sb1.p_sb.is_blank) and (sb1.n_sb and sb1.n_sb.is_blank): continue
                # compact with "I am ..."
                if (sb1.p_sb and sb1.p_sb.is_blank) and (sb1.relative_to_current(-2) and sb1.relative_to_current(-2).string == 'I'): continue
        return True

    @classmethod
    def is_normal_english_word(cls, word):
        if word.count(" "): return False

        return is_regular_word(word)

    @classmethod
    def unnormal_words_count(cls, sentence, inspect=False):
        if inspect: print "[unnormal_words_count]", sentence

        c = 0
        for sb1 in SplitBlockGroup.extract(sentence):
            if inspect: print [sb1]
            if sb1.is_letter and (not sb1.is_regular):
                c += 1
        return c

    @classmethod
    def select_most_fit_sentence(cls, items, read_attr_lambda=lambda item:item, base_chars_len=None):
        if False: #base_chars_len:
            items = [i1 for i1 in items if chars_len(i1[0]) == base_chars_len]

        # select min_unnormal_words_count result
        # select shortest result
        # select least blank count
        items = sorted(items, key = lambda result1: ( \
                                                      SentenceProcess.unnormal_words_count(read_attr_lambda(result1)), \
                                                      len(read_attr_lambda(result1).strip()), \
                                                      read_attr_lambda(result1).count(" ") \
                                                    ) \
                         )

        return items
