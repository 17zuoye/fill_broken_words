# -*- coding: utf-8 -*-

from collections import defaultdict
import re
import math
import itertools
from etl_utils import uniq_seqs

select_type = lambda item: re.compile("\.([a-z]+)'", re.IGNORECASE).findall(str(type(item)))[0]


def possible_connection_suggests(blanks_vs_fill_groups):
    result_len = len(set([i1[1] for i1 in blanks_vs_fill_groups]))
    final_results = []

    def select_one_link_blank_with_fill(blanks_vs_fill_groups, pre_result1=[]):
        fill_to_blanks, blank_to_fills = TwoLinksDict.extract_with_marked(blanks_vs_fill_groups, pre_result1)

        blanks = [blank1 for blank1 in blank_to_fills.keys() if blank1.marked is False]
        select_blanks_len = int(round(math.sqrt(len(blanks))))
        select_blanks = sorted(blanks, key = \
                lambda blank1: (len(blank1), len(blank1.items())))[0:select_blanks_len]

        for blank1 in select_blanks:
            fill2s = blank1.unmarked_items()
            if len(fill2s):
                # TODO maybe blank1 has two or more fill2s
                blank1.marked, fill2s[0].marked = True, True

                pre_result2 = pre_result1 + [ [blank1, fill2s[0]] ]

                if result_len == len(pre_result2):
                    final_results.append(pre_result2)
                else:
                    select_one_link_blank_with_fill(blanks_vs_fill_groups, pre_result2)

    select_one_link_blank_with_fill(blanks_vs_fill_groups)

    final_results = uniq_seqs(final_results, lambda result1: tuple(sorted([str(s1) for s1 in itertools.chain(*result1)])) )

    final_results = [ [ [result1[0].item, result1[1].item] for result1 in results1] for results1 in final_results ]

    return final_results



class TwoLinksDict(defaultdict):

    @classmethod
    def extract_with_marked(self, blanks_vs_fill_groups, marked_items=[]):
        flatten_marked_items = list(itertools.chain(*marked_items))

        fill_to_blanks = FillToBlanksDict(list)
        blank_to_fills = BlankToFillsDict(list)

        # prepare data
        for blanks_vs_fill_group1 in blanks_vs_fill_groups:
            blank1 = Blank.fetch(blanks_vs_fill_group1[0], blank_to_fills)
            fill1  = Fill .fetch(blanks_vs_fill_group1[1], fill_to_blanks)

            # reset .marked
            blank1.marked = bool(blank1 in flatten_marked_items)
            fill1 .marked = bool(fill1  in flatten_marked_items)

            blank1.append(fill1)
            fill1.append(blank1)

        return [fill_to_blanks, blank_to_fills]


class FillToBlanksDict(TwoLinksDict): pass
class BlankToFillsDict(TwoLinksDict): pass

class String(object):

    def __init__(self, item1, dict1):
        """ Fill and Blank are linked by self.fill_blank_dict. """
        self.item = item1
        self.fill_blank_dict = dict1
        self.marked = False

    def __str__(self): return str(self.item)
    def __len__ (self): return len(str(self))
    def __eq__(self, another):
        if type(another) != type(self): return False
        # depend on item's __eq__ method
        return self.item == another.item

    def __repr__(self): return "<%s \"%s\" marked=%s>" % (select_type(self), self.item, self.marked)

    def append(self, item1): self.fill_blank_dict[self].append(item1)
    def items(self): return self.fill_blank_dict[self]
    def unmarked_items(self): return [i1 for i1 in self.items() if not i1.marked]
    def   marked_items(self): return [i1 for i1 in self.items() if i1.marked]

    store = dict()

    @classmethod
    def fetch(cls, str1, dict1):
        if (str1 in cls.store) and \
                (cls.store[str1].fill_blank_dict is dict1):
            return cls.store[str1]

        cls.store[str1] = cls(str1, dict1)
        return cls.store[str1]

class Fill(String): pass
class Blank(String): pass
