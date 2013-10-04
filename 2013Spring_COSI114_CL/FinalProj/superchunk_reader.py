import re

from nltk.corpus.reader import BracketParseCorpusReader
from nltk.tree import Tree

# This lexer pattern is complicated by a few things. First, ")" is both a
# valid word and a valid part of speech tag, and so needs to be carefully
# distinguished from a ")" that represents the end of a tree. Second, "/"
# may appear within a word if it is escaped with a "\". (We should probably
# unescape the latter, but none of the NLTK methods do so, and so we
# won't, either.)
def str2tree(s, lex=re.compile(r"""\((?P<node>\w+)
                                 | (?P<word>(?:[^/\s]|\/)+)/(?P<pos>\)|[^\)\s]+)
                                 | \)""",
                               re.VERBOSE)):
    """Build a tree from a bracketed string representation.
    Trees are delimited by parentheses, and an opening parenthesis
    must be immediately followed by a node label. Words should be tagged
    with a part-of-speech label in the usual `word/pos' format."""
    stack = []
    for match in lex.finditer(s):
        token = match.group()
        if "/" in token:
            stack[-1].append((match.group("word"), match.group("pos").upper()))
        elif token[0] == "(":
            tree = Tree(match.group("node"), [])
            if stack:
                stack[-1].append(tree)
            stack.append(tree)
        elif token == ")":
            tree = stack.pop()
            if not stack:
                return tree
        else:
            raise ValueError("parse error: '%s'" % token)

class SuperchunkCorpusReader(BracketParseCorpusReader):
    """A corpus reader for Superchunked data."""
    def _parse(self, s):
        return str2tree(s)

    # Chunked? Parsed? Call it what you like.
    def chunked_sents(self, *args, **kwargs):
        return self.parsed_sents(*args, **kwargs)

def tree2iob(x, prefix="O", label="", super_prefix="O", super_label="",
             issuperchunk=lambda tree: tree.node=="SNP",
             issentence=lambda tree: tree.node=="S"):
    """Given a tree containing chunks and superchunks, yield tuples of the
    form (word, POS-tag, chunk-IOB-tag, superchunk-IOB-tag)."""
    if isinstance(x, Tree):
        if issuperchunk(x):
            super_prefix = "B-"
            super_label = x.node
        elif not issentence(x):
            prefix = "B-"
            label = x.node
        for child in x:
            for tag in tree2iob(child, prefix, label,
                                super_prefix, super_label,
                                issuperchunk, issentence):
                yield tag
            if prefix == "B-": prefix = "I-"
            if super_prefix == "B-": super_prefix = "I-"
    else:
        yield (x[0], x[1], prefix+label, super_prefix+super_label)

if __name__ == "__main__":
    from nltk.corpus import treebank_chunk as corpus

    # Ensure that str2tree correctly parses the string representations
    # of all trees in the chunked Treebank.
    for i, t in enumerate(corpus.chunked_sents()):
        assert str2tree(str(t)) == t, "incorrect parse for sentence %d" % i
