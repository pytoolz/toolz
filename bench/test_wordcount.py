from toolz.curried import *
import os
import subprocess

import pytest

SHAKESPEARE_TXT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'shakespeare.txt')
SHAKESPEARE_URL = 'http://www.gutenberg.org/files/100/100-0.txt'


def _ensure_shakespeare():
    """Download shakespeare.txt next to this file if it is missing.

    Return True if the file is available afterwards. The wget exit
    code is checked explicitly: a non-zero exit code, or a still
    missing file, means the download did not succeed.
    """
    if os.path.exists(SHAKESPEARE_TXT):
        return True
    result = subprocess.run(
        ['wget', SHAKESPEARE_URL, '-O', SHAKESPEARE_TXT])
    return result.returncode == 0 and os.path.exists(SHAKESPEARE_TXT)


def stem(word):
    """ Stem word to primitive form """
    return word.lower().rstrip(".,:;'-" ).lstrip("\"'")

wordcount = comp(frequencies, map(stem), concat, map(str.split))

def test_shakespeare():
    if not _ensure_shakespeare():
        pytest.skip(
            'bench/shakespeare.txt is unavailable and downloading it '
            'with wget failed; skipping test_shakespeare')
    with open(SHAKESPEARE_TXT) as f:
        counts = wordcount(f)
