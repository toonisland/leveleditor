from toontown.compiler.dna.components.DNAGroup import DNAGroup
from toontown.compiler.dna.base.DNAPacker import *


class DNADoor(DNAGroup):
    COMPONENT_CODE = 17

    def __init__(self, name):
        DNAGroup.__init__(self, name)

        self.code = ''
        self.color = (1, 1, 1, 1)

    def setCode(self, code):
        self.code = code

    def setColor(self, color):
        self.color = color

    def traverse(self, recursive=True, verbose=False):
        packer = DNAGroup.traverse(self, recursive=False, verbose=verbose)
        packer.name = 'DNADoor'  # Override the name for debugging.
        packer.pack('code', self.code, STRING)
        packer.packColor('color', *self.color)
        return packer
