import os
import time
import random
import hashlib
import subprocess
from subprocess import call
import StringIO

from settings import ROOT

ROOT = '/home/akellehe/projects/julian/'

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
    Converts a tagged sentence in NLTK format to a string of the format required by the collins parser. For lookups you can do nltk.help.brown_tagset() or nltk.help.upenn_tagset()
    
    :param list(tuple(str,str)): A pos tagged sentence in NLTK format.
    
    :rtype str: The sentence converted to collins' format.
    """
    simplified = []
    for word, pos in nltk_sent:
        if pos in ( 'AT', 'CS' ):
            pos = 'DT'
        elif pos == 'CD': # e.g. 20, 100, 10%
            pos = 'JJ'
        elif pos == 'NR': # Not recognized?
            pos = 'NN' # Noun. 
        elif pos == 'PPS': # Pronoun; it
            pos = 'PRP' # Personal pronoun
        elif pos == 'HVD': # Have, past tense.
            pos = 'VBD' # A verb, past tense
        elif pos == 'PP$': # Determiner, possessive
            pos = 'PRP$' # pronoun, possessive
        elif pos == 'OD': # Numeral, ordinal
            pos = 'JJ' # Adjective
        else:
            print "START:" + str( pos ) + ":END"
        simplified += [(word, pos)]
    return unicode( u"%s " % len(simplified) + u" ".join( i for i in [ u"%s %s" % j for j in simplified ]))


class CollinsResult:
    
    __maximal_depth = 0
    
    def __init__(self, s):
        self.s = s
        self.length = len(s)

    def parse(self, entry_callback=None, exit_callback=None):
        nesting = 0
        token_start = 0
        token_stop = 0
        last_entry_result = None
        last_exit_result = None
        for i in range(self.length):
            if self.s[i] == '(':
                if i+1 < self.length and self.s[i+1] == '/':
                    continue
                nesting += 1
                token_start = i
                if entry_callback:
                    last_entry_result = entry_callback((token_start, token_stop), nesting, i)
            elif self.s[i] == ')':
                if i+1 < self.length and self.s[i+1] == '/':
                    continue
                nesting -= 1
                token_stop = i
                if exit_callback:
                    last_exit_result = exit_callback((token_start, token_stop), nesting, i)
        return ( last_entry_result, last_exit_result )
        

    def maximal_depth(self):
        if self.__maximal_depth:
            return self.__maximal_depth

        nesting = 0
        get_max = lambda t, n, i: n if n > nesting else nesting
                
        self.__maximal_depth, nothing = self.parse( get_max )

        return self.__maximal_depth
    
    
    def get_token_of_length(self, seed, length):
        hash = hashlib.sha1(seed).hexdigest()
        if length < 40 and length > 6:
            return ' >>' + str(hash[0:length-6]) + '<< '
        elif length > 40:
            filler = ' ' * (length - 6 - 40)
            return ' >>' + str(hash) + filler + '<< '
        else:
            raise Exception( "Bad length for replacement: %s" % length )
        
        
    def parse_to_trees(self):
        maximal_depth = self.maximal_depth()
        o = [self.s]
        print o
        for depth in range(maximal_depth,-1,-1):
            # Need to loop until all replacements are final at this depth
            def exit_callback(token, nesting, index):
                if nesting == depth:
                    start, stop = token
                    print start, stop
                    t = self.get_token_of_length(o[0][start:stop], stop - start)
                    o[0] = o[0].replace(o[0][start:stop], t)
                    print o[0]
            self.parse(exit_callback=exit_callback)

    
def collins_to_tree(collins_result_str="()"):
    """
        (TOP~confirmed~1~1 (S~confirmed~2~2 (NPB~Korea~2~2 North/NNP Korea/NNP ) (VP~confirmed~4~1 confirmed/VBD (PP~on~2~1 on/IN (NPB~Tuesday~1~1 Tuesday/NNP ) ) (SBAR-A~that~2~1 that/IN (S-A~had~2~2 (NPB~it~1~1 it/PRP ) (VP~had~3~1 had/VBD (VP-A~conducted~2~1 conducted/VBN (NPB~test~5~5 its/PRP$ third/JJ ,/PUNC, long-threatened/NN nuclear/JJ test/NN ,/PUNC, ) ) (PP~according~2~1 according/VBG (PP-A~to~2~1 to/TO (NPB~service~5~5 the/DT official/JJ KCNA/NN news/NN service/NN ,/PUNC, ) ) ) ) ) ) (SG~posing~1~1 (VP~posing~3~1 posing/VBG (NP-A~challenge~2~1 (NPB~challenge~3~3 a/DT new/JJ challenge/NN ) (PP~for~2~1 for/IN (NPB~administration~3~3 the/DT Obama/NN administration/NN ) ) ) (PP~in~2~1 in/IN (NP-A~effort~2~1 (NPB~effort~2~2 its/PRP$ effort/NN ) (SG~to~1~1 (VP~to~2~1 to/TO (VP-A~keep~3~1 keep/VB (NPB~country~2~2 the/DT country/NN ) (PP~from~2~1 from/IN (SG-A~becoming~1~1 (VP~becoming~2~1 becoming/VBG (NPB~power~4~4 a/DT full-fledged/JJ nuclear/JJ power/NN ./PUNC. ) ) ) ) ) ) ) ) ) ) ) ) ) ) 
    """
    c = CollinsResult(collins_result_str)
    c.parse_to_trees()
    

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