# -*- coding: utf-8 -*-

# 组合算法的问题之王

# http://stackoverflow.com/questions/3788870/how-to-check-if-a-word-is-an-english-word-with-python?rq=1

# 如果原文本的空格不明显，可以先用单词表进行适当修复 做填入的空格。

# 如果str1和pattern结合后正确，而与其他没有结果，那么就代入而为新字符串。用于解决组合数目过多的贪婪算法。这个才是效率最高的算法。

# maybe 其实可以对有些组合做优先处理的。

import time
import itertools
import copy
from bunch import Bunch

from .utils import chars_len, ld, is_regular_word
from split_block import SplitBlock, SplitBlockGroup, Apart
from .patterns_vs_word import PatternsVsWord, PatternsVsWordGroup
from .sentence_process import SentenceProcess
from .params_strs import ParamsStrs
from .possible_connection_suggests import possible_connection_suggests

from etl_utils import ItertoolsUtils, singleton

@singleton()
class FillBrokenWordsClass(SentenceProcess):
    """
    Broken words should must be separated by two parts that one has only one char, or individual chars.

    Notice:
    processsed type are strs, not unicode.
    """

    def process(self, sentence, strs, inspect=False):
        if not len(strs): raise Exception("\"strs\" should at least have one item.")

        env = Bunch()
        env.sentence         = sentence
        env.inspect          = inspect

        # 1. generate SplitBlock list
        self.generate_SplitBlock_list(env)

        # 2. fix params strs
        env.params_strs = ParamsStrs(strs)
        env.params_strs.load_env(env.split_block_group)

        #env.base_chars_len = chars_len(env.params_strs.original_strs + [env.sentence])

        self.fix_params_strs(env)

        # 3. generate possible patterns, for multiple fill-able BLANKS.
        self.generate_possible_patterns_with_strs_list(env)

        # 4. generate possible patterns
        self.generate_candidate_patterns_vs_word_groups_s(env)

        # 5. generate regular sentence
        results = self.generate_regular_sentence(env)

        results = SentenceProcess.select_most_fit_sentence(results, read_attr_lambda=lambda item: item[0]) #, base_chars_len=env.base_chars_len)
        if env.inspect: print "[results] len", len(results)
        return results



    def generate_SplitBlock_list(self, env):
        # 1. generate SplitBlock list
        env.split_block_group = SplitBlockGroup.extract(env.sentence)

        if env.inspect: print "[split_block_group]", env.split_block_group; print


    def fix_params_strs(self, env):
        # 2. fix params strs
        if (env.params_strs.original_len != env.split_block_group.original_fillblank_length) and env.params_strs.is_all_individual_chars:
            # e.g. ["c      t  ", ["a", "o"], "coat  "] => ["oa", "ao"]
            # e.g. ["f      k (  叉  )", ["o", "r"], "fork (  叉  )"],
            if env.split_block_group.original_fillblank_length < env.params_strs.original_len:
                # 思路2. from lianhua. 把破碎单词用占位符替代

                # compact with ["boo", ["k"], "book"]
                if env.split_block_group.original_fillblank_length != 0:
                    env.params_strs[:] = []

                    split_size = [env.split_block_group.original_fillblank_length]
                    # -2 after fix_blanks_if_only_one_item
                    if (env.split_block_group.broken_letters_count() == 2) and env.split_block_group[-2].is_letter:
                        split_size.append(2)

                    # compact with ["ch    mn", ["e", "i", "y"], "chimney"]
                    if env.inspect: print "[split_size]", split_size
                    for size1 in split_size:
                        strs_order_combinations = ItertoolsUtils.split_seqs_by_size(range(env.params_strs.original_len), size1)
                        if env.inspect: print "[strs_order_combinations]", strs_order_combinations

                        for p1 in itertools.permutations(env.params_strs.original_strs):
                            for strs_order_combination1 in strs_order_combinations:
                                env.params_strs.append([ \
                                                     [''.join([p1[strs_order_combination3] for strs_order_combination3 in strs_order_combination2])][0] \
                                                 for strs_order_combination2 in strs_order_combination1 \
                                             ])

                    env.params_strs[:] = [tuple(s1) for s1 in env.params_strs]

            # e.g. ["t        b        e", ["a", "l"], "table"]
            # e.g. ["h              l", ["o", "e"], "hole"]
            #if (env.split_block_group.original_fillblank_length >= env.params_strs.original_len) and (env.params_strs.original_len > 1):
            if len(env.params_strs.original_strs) <= 3:
                env.params_strs += list(itertools.permutations(env.params_strs.original_strs))
                env.params_strs[:] = list(set(env.params_strs[:]))
        else:
            env.params_strs[:] = list(itertools.permutations(env.params_strs))

        if env.inspect: print "[params_strs:%i] %s ..." % (len(env.params_strs), env.params_strs[0:10])
        env.params_strs[:] = list(set(env.params_strs))
        env.params_strs_uniq_one = [i1[0] for i1 in env.params_strs] if env.params_strs.has_merged_at_least_one else env.params_strs[0]

        env.min_groups_len = min(env.split_block_group.original_fillblank_length, len(env.params_strs_uniq_one)) or 1 # compact wtih ["boo", ["k"], "book"]
        # Compact with when generate candidate_patterns_vs_word_groups_s
        # For current, one word only have to fill-blank at most.
        if env.min_groups_len > 1: env.min_groups_len -= 1


    def generate_possible_patterns_with_strs_list(self, env):
        # 3. generate possible patterns, for multiple fill-able BLANKS.
        possible_patterns_map = env.split_block_group.generate__possible_patterns_map(env.params_strs)

        # 3.1. group possible patterns
        possible_patterns_groups = possible_patterns_map.values()

        # 3.1.1 filter unpossible patterns_group
        to_remove_idxes = []
        new_possible_patterns_groups = []
        if env.inspect: print "before [possible_patterns_groups]", possible_patterns_groups
        for idx1, g1 in enumerate(possible_patterns_groups):
            # e.g. [[<<<#string#="f", hash=669352, [1 : 276-276], _type=letter, can_fill=False>>>, None]]
            is_remove_g1 = True
            for i1 in g1:
                # compact with ["s      l      d ", ["a", "a"], "salad "]
                if i1.count(None) == env.split_block_group.original_fillblank_length: new_possible_patterns_groups.append([i1])

                # e.g. [<<<#string#="f", hash=669352, [1 : 276-276], _type=letter, can_fill=False>>>, None]
                # 20140616 if not (i1.count(None) == 1): continue
                # only filter with one None field patterns
                for str1 in env.params_strs_uniq_one:
                    i1_copy = i1[:]
                    if not None in i1_copy: continue
                    i1_copy[i1_copy.index(None)] = str1
                    word2 = ''.join([str(i2 or '') for i2 in i1_copy])
                    if is_regular_word(word2):
                        is_remove_g1 = False
            if is_remove_g1: to_remove_idxes.append(idx1)
        for idx1, g1 in enumerate(possible_patterns_groups):
            if idx1 not in to_remove_idxes:
                new_possible_patterns_groups.append(g1)
        possible_patterns_groups = new_possible_patterns_groups
        if env.inspect: print "after [possible_patterns_groups]", possible_patterns_groups

        # 3.1.2 permutations all possible groups
        possible_patterns_list = list(itertools.permutations(possible_patterns_groups))

        # TODO maybe dont flatten, just groups
        possible_patterns_list = [i2 for i1 in possible_patterns_list for i2 in (len(i1) and i1[0] or [])] # turn set into list, which caused by itertools.permutations

        # 3.1.3. uniq possible_patterns_list, their strs is same.
        word_with_underscore_group = set([])
        old_possible_patterns_list = possible_patterns_list
        possible_patterns_list = []
        for possible_patterns1 in old_possible_patterns_list:
            word_with_underscore1 = "".join([ ( (i1 and str(i1)) or "_" ) for i1 in possible_patterns1])
            if word_with_underscore1 in word_with_underscore_group:
                continue
            else:
                possible_patterns_list.append(possible_patterns1)
                word_with_underscore_group.add(word_with_underscore1)

        if env.inspect:
            print; print "[possible_patterns_list]"
            for idx, ppl1 in enumerate(possible_patterns_list):
                print idx, ppl1; print

        # 3.2. group possible patterns with params_str1
        env.possible_patterns_with_strs_list = list(itertools.product(possible_patterns_list, env.params_strs))

    def generate_candidate_patterns_vs_word_groups_s(self, env):
        # TODO slow!!!
        candidate_patterns_vs_word_groups = []
        __uniq_word_dict = dict()
        if env.inspect: print "[env.possible_patterns_with_strs_list]", len(env.possible_patterns_with_strs_list)
        for patterns_with_strs1 in env.possible_patterns_with_strs_list:
# 1440 个，所以可能慢, 其他都不到100, 甚至个位数
            patterns2, strs2 = patterns_with_strs1
            patterns2 = copy.deepcopy(patterns2) # avoid to modify same SplitBlockGroup
            # TODO patterns2 is abstract `instance` type, not just after deepcopy, but all parts of the processing.
            strs_read_idx = 0 # avoid to modify sharing variables
            for idx3, p3 in enumerate(patterns2):
                if len(strs2) <= strs_read_idx: break
                if p3 is None:
                    patterns2[idx3] = strs2[strs_read_idx]
                    strs_read_idx += 1

            word1 = ''.join([str(i1) for i1 in patterns2])
            if word1 in __uniq_word_dict:
                continue
            else:
                __uniq_word_dict[word1] = True

            # select regular words
            if is_regular_word(word1):
                candidate_patterns_vs_word_groups.append(PatternsVsWord(patterns2, word1))
                if env.inspect: print "[word1]", word1

        if env.inspect:
            print
            print "[candidate_patterns_vs_word_groups]"
            print "*"*30
            for i1 in candidate_patterns_vs_word_groups: print i1
            print "*"*30
            print

        # dont compact those condition, it'll return []
        # 1. not ["s      l      d ", ["a", "a"], "salad "] has same answers
        # 2. or have ["the F      bidden C   ty", ["i", "o", "r"], "the Forbidden City"] any merge
        if not (env.params_strs.is_all_same_chars or env.params_strs.has_merged_at_least_one \
                or ((env.split_block_group.fillblank_length() - env.split_block_group.original_fillblank_length) == 2) ):
                # compact with ["t        b        e", ["a", "l"], "table"]
            candidate_patterns_groups = [Apart.process(i1.patterns) for i1 in candidate_patterns_vs_word_groups]
            uniq_results1 = possible_connection_suggests(candidate_patterns_groups)
            apart_list1 = list(itertools.chain(*uniq_results1))

            new_candidate_patterns_vs_word_groups = []
            for candidate_patterns_vs_word_group1 in candidate_patterns_vs_word_groups:
                ab = Apart.process(candidate_patterns_vs_word_group1.patterns)
                if ab in apart_list1:
                    new_candidate_patterns_vs_word_groups.append(candidate_patterns_vs_word_group1)

            candidate_patterns_vs_word_groups = new_candidate_patterns_vs_word_groups

# TODO slow!!!
        env.candidate_patterns_vs_word_groups_s = []
        for group_size in range(env.min_groups_len, env.split_block_group.original_fillblank_length+1) or [1]: # compact wtih ["boo", ["k"], "book"]
            gs = [PatternsVsWordGroup(g1) for g1 in itertools.combinations(candidate_patterns_vs_word_groups, group_size)]
            gs = [g1 for g1 in gs if not g1.has_common_items()]
            env.candidate_patterns_vs_word_groups_s.extend(gs)
        if env.inspect: print "[candidate_patterns_vs_word_groups_s] %i items" % len(env.candidate_patterns_vs_word_groups_s)
        for c1 in env.candidate_patterns_vs_word_groups_s[0:20]:
            if env.inspect: print c1
        if env.inspect: print


    def generate_regular_sentence(self, env):
# TODO slow!!!
        results = []
        for candidate_patterns_vs_word_groups1 in env.candidate_patterns_vs_word_groups_s:
            if env.inspect: print "[candidate_patterns_vs_word_groups1]", candidate_patterns_vs_word_groups1
            if env.inspect: print
            # avoid to modify the same "split_block_group" in each loop, cause dont need to modify the original "split_block_group"
            split_block_group_copy = env.split_block_group.deepcopy()

            # compact with "f      k (  叉  )" that has only a center part.
            if env.params_strs.has_merged_at_least_one and (env.split_block_group.original_fillblank_length == 1) and (len(candidate_patterns_vs_word_groups1[0].patterns) == 1):
                if env.inspect: print "[env.sentence]", env.sentence
                for idx1, sb1 in enumerate(split_block_group_copy):
                    if sb1.is_blank and sb1.can_fill:
                        split_block_group_copy[idx1] = " " + candidate_patterns_vs_word_groups1[0].word + " "
            else:
                split_block_group_copy.fill__patterns_vs_word_groups(candidate_patterns_vs_word_groups1)


            filled_sort = ''.join(sorted(list(''.join(filter(lambda i1: isinstance(i1, str), candidate_patterns_vs_word_groups1[0].patterns)))))
            original_sort = ''.join(sorted(list(''.join(env.params_strs.original_strs))))
            is_all_params_strs_filled = filled_sort == original_sort

            # 5.4 append into results
            if is_all_params_strs_filled:
                results.append([split_block_group_copy.concat_items(), candidate_patterns_vs_word_groups1])

        return results

FillBrokenWords = FillBrokenWordsClass()
