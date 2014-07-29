Fill broken words
===============================
Consider there's a sentence, which has a half part of one word outside of it, e.g. ["How many s                 of pizza do you want?", ["lices"]], so we need to fix it correctly.

Algorithm Processing Graph
-------------------------------

```txt
                                  Sentence                                                           Strs
                                     ||                                                               ||
                  SplitBlock.extract ||                                                               \/
                                     ||                                                   Generate strs permutations
                                     \/                                                               ||
                                SplitBlockGroup                                                       \/
                                      |                                                              /
       |------------|-----------|-----------|-----------|-------|                                   /
       |            |           |           |           |       |  ---------------------------->>>-/
  [SplitBlock, SplitBlock, SplitBlock, SplitBlock, SplitBlock, ... ]                              ||
                                                                                                  \/
                                     ||                                                 Generate possible patterns list
                                     ||                                                           ||
                                     ||                                                           \/
                                     ||                                                 Generate candidate pattern with str groups
                                     ||                                                           ||
                                     ||                                                           ||
                                     ||                                                           ||
                                     ||                                                           ||
                                     \/ --------------------------------------------------------  \/
                                                               ||
                                                               \/
                                                        Merge into results

```



Example
-------------------------------

```python
from fill_broken_words import FillBrokenWords

FillBrokenWords.process("Jim is f                 E                 . ", ["ngland", "rom"])

"""
[split_block_group] [<<<#string#="Jim", hash=904651, length=3, _type=letter, pos_begin=0, pos_end=3, pre_split_block=-9223372036586252507, next_split_block=620354, can_fill=False>>>, <<<#string#=" ", hash=620354, length=1, _type=blank, pos_begin=4, pos_end=4, pre_split_block=904651, next_split_block=762524, can_fill=False>>>, <<<#string#="is", hash=762524, length=2, _type=letter, pos_begin=5, pos_end=6, pre_split_block=620354, next_split_block=620376, can_fill=False>>>, <<<#string#=" ", hash=620376, length=1, _type=blank, pos_begin=7, pos_end=7, pre_split_block=762524, next_split_block=620474, can_fill=False>>>, <<<#string#="f", hash=620474, length=1, _type=letter, pos_begin=8, pos_end=8, pre_split_block=620376, next_split_block=738519, can_fill=False>>>, <<<#string#="                 ", hash=738519, length=17, _type=blank, pos_begin=9, pos_end=25, pre_split_block=620474, next_split_block=738516, can_fill=True>>>, <<<#string#="E", hash=738516, length=1, _type=letter, pos_begin=26, pos_end=26, pre_split_block=738519, next_split_block=580332, can_fill=False>>>, <<<#string#="                 ", hash=580332, length=17, _type=blank, pos_begin=27, pos_end=43, pre_split_block=738516, next_split_block=738644, can_fill=True>>>, <<<#string#=".", hash=738644, length=1, _type=other, pos_begin=44, pos_end=44, pre_split_block=580332, next_split_block=738668, can_fill=False>>>, <<<#string#=" ", hash=738668, length=1, _type=blank, pos_begin=45, pos_end=45, pre_split_block=738644, next_split_block=-9223372036586252507, can_fill=False>>>]

[params_strs] [('ngland', 'rom'), ('rom', 'ngland')]

[possible_patterns_list]
0 [<<<#string#="E", hash=738516, length=1, _type=letter, pos_begin=26, pos_end=26, pre_split_block=738519, next_split_block=580332, can_fill=False>>>, None]

1 [<<<#string#="f", hash=620474, length=1, _type=letter, pos_begin=8, pos_end=8, pre_split_block=620376, next_split_block=738519, can_fill=False>>>, None]

[word1] England
[word1] Erom
[word1] fngland
[word1] from

[candidate_pattern_with_str_groups]
******************************
[[<<<#string#="E", hash=738516, length=1, _type=letter, pos_begin=26, pos_end=26, pre_split_block=738519, next_split_block=580332, can_fill=False>>>, 'ngland'], 'England']
[[<<<#string#="f", hash=620474, length=1, _type=letter, pos_begin=8, pos_end=8, pre_split_block=620376, next_split_block=738519, can_fill=False>>>, 'rom'], 'from']
******************************

[indexes] [6, 7]
[indexes] [4, 5]
[results] [['Jim is from England . ', ['England', 'from']]]
"""

# => [['Jim is from England . ', ['England', 'from']]]

```

see more examples in tests.


License
-------------------------------
MIT. David Chen at 17zuoye.
