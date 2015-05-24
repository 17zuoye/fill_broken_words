# -*- coding: utf-8 -*-

# 处理后的copus应该只更新对应部分，其他部分不动。

import os
import sys
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)


import unittest
from fill_broken_words.fill_broken_words import FillBrokenWords, possible_connection_suggests


class TestFillBrokenWords(unittest.TestCase):

    def test_fill_broken_words(self):
        corpus = [
                    #["Hello! I am Alice. This is a p          of my family.  We are having a picnic in the park. We are sitting on  the g         grass. Look, this is my grandmother. She  is old. She likes eating c        . This is my mother.  She is kind and dear. She likes cooking. This is my  f        . He is tall. He likes cola. This is my  brother, Tom. He is ten. He likes playing football. He  can play it very well. This is m        . I'm small. I  like eating apples. We are happy together.", ["akes", "ather", "e", "icture", "reen"], "Hello! I am Alice. This is a picture of my family.  We are having a picnic in the park. We are sitting on  the green grass. Look, this is my grandmother. She  is old. She likes eating cakes . This is my mother.  She is kind and dear. She likes cooking. This is my  father . He is tall. He likes cola. This is my  brother, Tom. He is ten. He likes playing football. He  can play it very well. This is me . I'm small. I  like eating apples. We are happy together."],
                    #["ex    r   se h     d    che   ir    d ", ["a", "e", "e", "ea", "i", "t"], "exercise headache tired "],
                    #["ex    r   se h     d    che   ir    d ", ["a", "e", "e", "ea", "应该为ci, 原文错误", "t"], "exercise headache tired "],

                    ["s      l      d ", ["a", "a"], "salad "],
                    ["boo", ["k"], "book"],
                    ["h   bb  ", ["o", "y"], "hobby"],
                    #["the F      bidden C   ty", ["i", "o", "r"], "the Forbidden City"],
                    ["—Can you             ? —Yes, I can.", ["i", "m", "s", "w"], "—Can you swim ? —Yes, I can."],
                    ["amera", ["c"], "camera"],
                    ["s       d    er", ["i", "l", "o"], "soldier"],
                    ["Don't w               . I can help you.", ["orry"], "Don't worry . I can help you."],

                    ["hell     ", ["o"], "hello"],
                    ###["he o", ["l", "l"], "hello"],

                    #["Jim is f                 E                 . ", ["ngland", "rom"], "Jim is from England . "],
                    ["c      t  ", ["a", "o"], "coat  "],
                    ["How many s                 of pizza do you want?", ["lices"], "How many slices of pizza do you want?"],
                    #["Welcome to o                 s                . ", ["chool", "ur"], "Welcome to our school . "],
                    ["f      k (  叉  )", ["o", "r"], "fork (  叉  )"],
                    ["a  k    te", ["i"], "a  kite"],
                    ["k       t     ", ["i", "e"], "kite"],
                    ["  ven", ["o"], "oven"],
                    ["t        b        e", ["a", "l"], "table"],

                    [" uby  ython", ["R", "P"], "Ruby Python"],
                    ["e    e        ", ["y"], "eye        "],

                    ["ki   ", ["ck"], "kick"],  # 5111b965a3109d262ad98d2f TODO 还是错了
                    ["fl       er", ["w", "o"], "flower"],
                    ["ch    mn", ["e", "i", "y"], "chimney"],
                    #[" p n (打开) ", ["e", "o"], "open (打开) "],
                    #["r  bb  t (兔)  ", ["a", "i"], "rabbit (兔)  "],
                    #["TV  pr   gr   mme", ["o", "a"], "TV  programme"],
                    #["bru", ["s", "h"], "brush"],
                    #["d   nn", ["e", "i", "r"], "dinner"],
                    ["h              l", ["o", "e"], "hole"],
                    ["  very", ["e"], "every"],
                    #["enci", ["p", "l"], "pencil"],
                    #["s    bw   y   ", ["u", "a"], "subway   "],
                    ["d         a picture", ["raw"], "draw a picture"],
                    ["s   fety r   les", ["a", "u"], "safety rules"],
                    ["Can you t   p    fast?", ["y", "e"], "Can you type fast?"],
                    ["l   phant", ["e", "e"], "elephant"],
                    ][1:11]  # :28] # [0:1] # 

        for sentence, strs, sentence2 in corpus:
            print "=" * 150
            print "[original sentence] \"%s\"" % sentence
            print
            results = FillBrokenWords.process(sentence, strs, True)
            print
            print "[tests]", results[0]
            self.assertEqual(results[0][0], sentence2)

    def test_process(self):
        results = possible_connection_suggests([
                             ["f", "akes"],
                             ["f", "ather"],
                             ["c", "akes"],
                             ["m", "akes"],
                             ["m", "e"],
                             ["p", "icture"],
                             ["p", "reen"],
                             ["He", "ather"],
                             ["on", "e"],
                             ["g", "ather"],
                             ["g", "reen"],
                            ])
        self.assertEqual(len(results), 1)
        self.assertEqual(sorted([(str(group1[0]) + str(group1[1])) for group1 in results[0]]), ['cakes', 'father', 'green', 'me', 'picture'])


if __name__ == '__main__':
    unittest.main()

# ["  cl    set        s    ster            d    sk    st    dy", ["e", "i", "o", "u"]]
