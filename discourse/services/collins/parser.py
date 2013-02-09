import os
import time
import random
import subprocess
from subprocess import call
import StringIO

from settings import ROOT

ROOT = '/home/joehill/projects/julian/'

COLLINS_ROOT = ROOT + 'vendor/COLLINS-PARSER/'
EVENTS_PATH  = COLLINS_ROOT + 'models/model%s/events.gz'
PARSER_PATH  = COLLINS_ROOT + 'code/parser'
GRAMMAR_PATH = COLLINS_ROOT + 'models/model%s/grammar'
TMP_FILE_DIR = ROOT + 'tmp'

def __write_tmp_file(tagged_sents):
    """
    Writes the tagged sentences to a file in the proper format for the collins parser to read.
    
    :param tagged_sents: The POS tagged sentences.
    
    :rtype str: The absolute path to the tmp file.
    """
    tmp_file_name = "%s.%s.%s" % ( time.time(), random.random(), '.collins_tagged' )
    with open(TMP_FILE_DIR + '/' + tmp_file_name, 'wb') as f:
        for s in tagged_sents:
            f.write( __nltk_sent_to_collins_sent(s) + u'\n' )
    return TMP_FILE_DIR + '/' + tmp_file_name

def __nltk_sent_to_collins_sent( nltk_sent ):
    """
    Converts a tagged sentence in NLTK format to a string of the format required by the collins parser.
    
    :param list(tuple(str,str)): A pos tagged sentence in NLTK format.
    
    :rtype str: The sentence converted to collins' format.
    """
    simplified = []
    for word, pos in nltk_sent:
        if pos in ( 'AT', 'CS' ):
            pos = 'DT'
        elif pos is 'CD': # e.g. 20, 100, 10%
            pos = 'JJ'
        simplified += [(word, pos)]
    return unicode( u"%s " % len(simplified) + u" ".join( i for i in [ u"%s %s" % j for j in simplified ]))

def build_trees(tagged_sents, beam_size=1000, punct_constraint=1, 
                distaflag=1, distvflag=1, npbflag=1, model=2, 
                timeout=120):
    """
    Takes a set of nltk tagged sentences, converts their format to collins tags, writes them to a file, and launches a blocking subprocess to build the appropriate parse tree with the collins parser.
    
    :param list(list(tuple(str,str))) tagged_sents: The nltk format pos tagged sentences
    :param int beam_size:  the size of the beam. 10000 is usual, 1000 will be faster at a slight cost in accuracy.
    :param int punct_constraint: 1 if the punctuation constraint is to be used, you will usually want this to be the case
    :param int distaflag: 1 for the adjacency condition in the distance measure to be used. This flag should almost certainly be set to be 1.
    :param int distvflag: 1 for the verb condition in the distance measure to be used. This flag should almost certainly be set to be 1.
    :param int npbflag: 1 for output format that can be scored against the the treebank. If it's set to 0 the output will include an extra level in some NPs
    :param int model: The collins model to use. 1-3. Defaults to 1.
    :param int timeout: The maximum length of time to hang waiting for the output file to be written.
    
    :rtype list(Tree): The nltk parse tree for the tagged sentence.
    """
    print tagged_sents
    tmp_file = __write_tmp_file(tagged_sents)
    
    p1 = subprocess.Popen( [ 'gunzip', '-c', EVENTS_PATH % model ], stdout=subprocess.PIPE )
    p2 = subprocess.Popen( [ PARSER_PATH, 
                            tmp_file, 
                            GRAMMAR_PATH % model, 
                            '%s' % beam_size,
                            '%s' % punct_constraint,
                            '%s' % distaflag,
                            '%s' % distvflag,
                            '%s' % npbflag ], 
                          stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    msg, err = p2.communicate()
    
    try: os.unlink(tmp_file)
    except: pass
    print msg
    return msg