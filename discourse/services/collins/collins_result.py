import hashlib
import re
from nltk.tree import Tree

class CollinsResult:

    
    __maximal_depth = 0
    __tree_refs = {}

    
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
                token_stop = i+1
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
        h = hashlib.sha1(seed).hexdigest()
        if length <= 46 and length > 6:
            return ' >>%s<< ' % str(h[0:length-6])
        elif length > 46:
            filler = '0' * (length - 40 - 6)
            return ' >>%s<< ' % (str(h) + filler)
        else:
            raise Exception("Bad length for replacement: %s" % length)


    def node_to_tree(self, node_string ):
        children = []
        print "NODE STRING:", node_string
        s = re.split(r'\s+', node_string[1:-1])
        node_value = s[0].split('~')[0]
        for tagged_word in s[1:]:
            if not tagged_word:
                continue
            split_word = tagged_word.split('/')
            if len(split_word) == 1:
                print "TAGGED WORD:", tagged_word
                children.append(self.__tree_refs[tagged_word])
            else:
                word, pos = tuple(["".join(split_word[0:-1]), split_word[-1]])
                children.append( Tree( pos, [word] ) )
                
        return Tree( node_value, children )


    def parse_to_trees(self): # TODO: This approach to parsing is inefficient.
        maximal_depth = self.maximal_depth()
        subtree = None
        for depth in range(maximal_depth,-1,-1):
            def exit_callback(token, nesting, index):
                if nesting == depth:
                    start, stop = token
                    subtree = self.node_to_tree( self.s[start:stop] )
                    t = self.get_token_of_length(self.s[start:stop], stop - start )
                    self.s = "%s%s%s" % ( self.s[0:start], t, self.s[stop:] )                    
                    self.__tree_refs[t.strip()] = subtree
                    self.__tree = subtree
                    
            self.parse(exit_callback=exit_callback)

        return self.__tree
