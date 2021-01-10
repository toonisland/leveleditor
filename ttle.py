""" OpenLevelEditor Base Class - Drewcification 091420 """

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText

from panda3d.core import loadPrcFile, loadPrcFileData

from tkinter import Tk, messagebox
from toontown.toonbase import ToontownGlobals

import asyncio
import argparse
import builtins
import os
import sys

class ToontownLevelEditor(ShowBase):
    notify = directNotify.newCategory("TIA Level Editor")
    APP_VERSION = "TIA"

    def __init__(self):

        # Load the prc file prior to launching showbase in order
        # to have it affect window related stuff
        loadPrcFile('editor.prc')

        builtins.userfiles = self.config.GetString('userfiles-directory')

        if not os.path.exists(userfiles):
            pathlib.Path(userfiles).mkdir(parents = True, exist_ok = True)

        # Check for -e or -d launch options
        parser = argparse.ArgumentParser(description = "Modes")
        parser.add_argument("--png", action = 'store_true', help = "Forces PNG resources mode, if this is not specified, "
                                                                   "it will automatically determine the format")
        parser.add_argument("--holiday", nargs = "*", help = "Enables holiday modes. [halloween or winter]")
        parser.add_argument("--hoods", nargs = "*", help = "Only loads the storage files of the specified hoods",
                            default = ['TT', 'DD', 'BR', 'DG',
                                       'DL', 'MM'])
        parser.add_argument("dnaPath", nargs = "?", help = "Load the DNA file through the specified path")

        args = parser.parse_args()
        loadPrcFileData("", "want-experimental true")
        loadPrcFileData("", "want-debug true")
        loadPrcFileData("", f"compiler libpandadna")
        if args.holiday:
            loadPrcFileData("", f"holiday {args.holiday[0]}")
        else:
            # If we don't specify png, we can search
            # we can use the eyes texture
            if os.path.exists("resources/phase_3/maps/eyes.jpg"):
                loadPrcFileData("", "png-textures false")
            elif os.path.exists("resources/phase_3/maps/eyes.png"):
                loadPrcFileData("", "png-textures true")
            else:
                messagebox.showerror(
                    message = "There was an error located resources!\n"
                              "Make sure you put the phase folders in the resources folder!")

        self.server = 0

        self.hoods = args.hoods
        # HACK: Check for dnaPath in args.hoods
        for hood in self.hoods[:]:
            if hood.endswith('.dna'):
                args.dnaPath = hood
                args.hoods.remove(hood)
                break

        # Check for any files we need and such
        self.__checkForFiles()

        # Import the main dlls so we don't have to repeatedly import them everywhere
        self.__importMainLibs()

        # Setup the root for Tkinter!
        self.__createTk()

        self.__addCullBins()

        # Now we actually start the editor
        ShowBase.__init__(self)
        aspect2d.setAntialias(AntialiasAttrib.MAuto)

        # Create the framerate meter
        flag = self.config.GetBool('show-frame-rate-meter', False)
        if flag:
            self.toggleFrameRateMeter(flag)

        from toontown.leveleditor import LevelEditor
        self.le = LevelEditor.LevelEditor()
        self.le.startUp(args.dnaPath)

    def setFrameRateMeter(self, flag):
        return

    def toggleFrameRateMeter(self, flag):
        if flag:
            if not self.frameRateMeter:
                self.frameRateMeter = OnscreenText(parent = base.a2dTopRight, text = '', pos = (-0.01, -0.05, 0.0),
                                                   scale = 0.05, style = 3, bg = (0, 0, 0, 0.4), align = TextNode.ARight,
                                                   font = ToontownGlobals.getToonFont())
                taskMgr.add(self.updateFrameRateMeter, 'fps')
        else:
            if self.frameRateMeter:
                self.frameRateMeter.destroy()
                self.frameRateMeter = None

    def updateFrameRateMeter(self, task):
        """
        Base code inspired from
        https://discourse.panda3d.org/t/trying-to-create-custom-fps-counter/25328/15
        """
        fps = globalClock.getAverageFrameRate()

        # Color is green by default
        color = (0, 0.9, 0, 1)

        # At or below 45 fps is yellow
        if fps <= 45:
            color = (1, 0.9, 0, 1)
        # At or below 30 fps is red
        elif fps <= 30:
            color = (1, 0, 0, 1)

        text = f'{round(fps, 1)} FPS'
        self.frameRateMeter.setText(text)
        self.frameRateMeter.setFg(color)

        return task.cont

    def __checkForFiles(self):
        # Make custom hood directory if it doesn't exist
        if not os.path.exists(f'{userfiles}/hoods/'):
            os.mkdir(f'{userfiles}/hoods/')
        # Make a maps directory if we don't have one
        if not os.path.isdir("maps"):
            os.mkdir("maps")
        # Make a Screenshots directory if we don't have one
        if not os.path.isdir("screenshots"):
            os.mkdir("screenshots")

    def __importMainLibs(self):
        builtin_dict = builtins.__dict__
        builtin_dict.update(__import__('panda3d.core', fromlist = ['*']).__dict__)
        builtin_dict.update(__import__('libotp', fromlist = ['*']).__dict__)
        builtin_dict.update(__import__('libtoontown', fromlist = ['*']).__dict__)

    def __createTk(self):
        tkroot = Tk()
        tkroot.withdraw()
        tkroot.title("TIA Level Editor - Toolbox")
        if sys.platform == 'win32':
            # FIXME: This doesn't work in other platforms for some reason...
            tkroot.iconbitmap("resources/phase_3/etc/icon.ico")

        self.tkRoot = tkroot

    def __addCullBins(self):
        cbm = CullBinManager.getGlobalPtr()
        cbm.addBin('ground', CullBinManager.BTUnsorted, 18)
        cbm.addBin('shadow', CullBinManager.BTBackToFront, 19)

# Run it
ToontownLevelEditor().run()
