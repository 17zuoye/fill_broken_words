# -*- coding: utf-8 -*-

class ParamsStrs(list):

    def __init__(self, strs1):
        super(ParamsStrs, self).__init__(strs1)

        self.original_strs           = strs1[:]
        self.original_len            = len(strs1)

        self.is_all_individual_chars = len(self) == len(''.join(self))
        self.is_all_same_chars       = (len(set(self)) == 1) and self.is_all_individual_chars

    def load_env(self, split_block_group1):
        self.has_merged_at_least_one = False

        if (self.original_len != split_block_group1.original_fillblank_length) and self.is_all_individual_chars:
            if split_block_group1.original_fillblank_length < self.original_len:
                self.has_merged_at_least_one = True
