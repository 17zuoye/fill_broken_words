# -*- coding: utf-8 -*-

from split_block import SplitBlock

class PatternsVsWord(object):

    def __init__(self, patterns, word):
        self.patterns = patterns
        self.word     = word

        filterd_split_block_list = filter(lambda sb1_or_str: isinstance(sb1_or_str, SplitBlock), self.patterns)
        self.pos_tuple = tuple([sb1.pos_begin for sb1 in filterd_split_block_list])

    def __repr__(self):
        return str([self.patterns, self.word])

    def has_common_with(self, another_patterns_vs_word):
        if not isinstance(another_patterns_vs_word, PatternsVsWord):
            raise Exception("%s should be a PatternsVsWord" % another_patterns_vs_word)

        return self.pos_tuple == another_patterns_vs_word.pos_tuple
