from toontown.compiler.dna.components.DNAGroup import DNAGroup
from toontown.compiler.dna.parser.parser import *
from toontown.compiler.dna.parser.tokens import *
from toontown.compiler.ply import yacc


class DNARoot(DNAGroup):
    def __init__(self, name='root', dnaStore=None):
        DNAGroup.__init__(self, name)

        self.dnaStore = dnaStore

    def read(self, stream):
        parser = yacc.yacc(debug=0, optimize=0)
        parser.dnaStore = self.dnaStore
        parser.root = self
        parser.parentGroup = self
        parser.modelName = None
        parser.modelType = None
        parser.parse(stream.read())
