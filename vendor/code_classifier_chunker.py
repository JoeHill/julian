import nltk
import os
from cPickle import load, dump

from nltk.corpus import conll2000

from settings import ROOT

chunker_path = ROOT + 'vendor/parsers/consecutive_np_chunker.pk1'
nltk.config_megam(ROOT + 'vendor/megam_i686.opt')

# Natural Language Toolkit: code_classifier_chunker
def npchunk_features(sentence, i, history):
    word, pos = sentence[i]
    if i == 0:
        prevword, prevpos = "<START>", "<START>"
    else:
        prevword, prevpos = sentence[i-1]
    return {'pos': pos, 'word': word, 'prevpos': prevpos}


class ConsecutiveNPChunkTagger(nltk.TaggerI): # [_consec-chunk-tagger]

    def __init__(self, train_sents):
        train_set = []
        for tagged_sent in train_sents:
            untagged_sent = nltk.tag.untag(tagged_sent)
            history = []
            for i, (word, tag) in enumerate(tagged_sent):
                featureset = npchunk_features(untagged_sent, i, history) # [_consec-use-fe]
                train_set.append( (featureset, tag) )
                history.append(tag)
        self.classifier = nltk.MaxentClassifier.train( # [_consec-use-maxent]
            train_set, algorithm='megam', trace=0)

    def tag(self, sentence):
        history = []
        for i, word in enumerate(sentence):
            featureset = npchunk_features(sentence, i, history)
            tag = self.classifier.classify(featureset)
            history.append(tag)
        return zip(sentence, history)

class ConsecutiveNPChunker(nltk.ChunkParserI): # [_consec-chunker]
    def __init__(self, train_sents):
        tagged_sents = [[((w,t),c) for (w,t,c) in
                         nltk.chunk.tree2conlltags(sent)]
                        for sent in train_sents]
        self.tagger = ConsecutiveNPChunkTagger(tagged_sents)

    def parse(self, sentence):
        tagged_sents = self.tagger.tag(sentence)
        conlltags = [(w,t,c) for ((w,t),c) in tagged_sents]
        return nltk.chunk.conlltags2tree(conlltags)

np_chunker = None
# Cache chunker to vendor
if os.path.exists(chunker_path):
    with open(chunker_path,'rb') as i:
        np_chunker = load(i)
else:
    train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])
    np_chunker = ConsecutiveNPChunker(train_sents)
    with open(chunker_path, 'wb') as o:
        dump(np_chunker, o, -1)


