from toolz.curried import *
import os

if not os.path.exists('bench/shakespeare.txt'):
    os.system('wget http://www.gutenberg.org/files/100/100-0.txt'
              ' -O bench/shakespeare.txt')


def stem(word):
    """ Stem word to primitive form """
    return word.lower().rstrip(",.!:;'-\"").lstrip("'\"")

wordcount = comp(frequencies, map(stem), concat, map(str.split))


def test_shakespeare():
    with open('bench/shakespeare.txt') as f:
        counts = wordcount(f)
