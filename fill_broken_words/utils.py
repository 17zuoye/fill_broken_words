# -*- coding: utf-8 -*-

from etl_utils import ld, is_regular_word

def chars_len(strs):
    if not isinstance(strs, list): strs = [strs]
    return len(''.join(re.compile("[a-z]+", re.IGNORECASE).findall( ''.join(strs) )))
