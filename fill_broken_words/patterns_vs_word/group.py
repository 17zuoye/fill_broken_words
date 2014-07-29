# -*- coding: utf-8 -*-

class PatternsVsWordGroup(list):

    def has_common_items(self):
        pos_tuples = [s2 for s1 in self for s2 in s1.pos_tuple]

        # 20140616
        #str_tuples = [s2 for s1 in self for s2 in s1.patterns if isinstance(s2, str)]

        return (len(pos_tuples) != len(set(pos_tuples)))
        #return (len(pos_tuples) != len(set(pos_tuples))) or \
        #        (len(str_tuples) != len(set(str_tuples)))
