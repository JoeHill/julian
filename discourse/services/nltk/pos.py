import nltk
import re
from cPickle import load

from settings import ROOT


def __load_tagger(name):
    tagger = None
    with open(ROOT + 'vendor/taggers/' + name + '.pk1') as i:
        tagger = load(i)
    return tagger


t3 = __load_tagger('t3')

def tag(s):
    """
    Tags a paragraph, s, with parts of speech.
    
    :param str s: A natural language paragraph.
    
    :rtype list(tuple(str, str)): The pos annotated paragraph.
    """
    sentences = nltk.sent_tokenize(s)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [t3.tag(sent) for sent in sentences]
    return sentences

def clean(s):
    """
    Preprocesses a string to be tagged. Removes erroneous whitespace. UTF-safe.
    
    :param str s: A string to be cleaned.

    :rtype str: The same string with erroneous whitespace removed.
    """
    s = re.sub( r"\s+", " ", s )
    s = re.sub( r"\s*$", "", s )
    s = re.sub( r"^\s*", "", s )
    return s