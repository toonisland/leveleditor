# StartCompiledGame will launch a compiled client by performing several key tasks along the way
# before handing everything over to ToontownStart

# Replace some modules that do exec:
import collections
collections.namedtuple = lambda *x: tuple

# This is included in the package by the client preparation script. It contains the
# configuration.
import gamedata

# Load all packaged config pages:
from panda3d.core import loadPrcFileData
for i,config in enumerate(gamedata.CONFIG):
    loadPrcFileData('Packaged Config Page #%d' % i, config)

# Everything's been done that needs to be, so let's start Toontown!
import ttle
