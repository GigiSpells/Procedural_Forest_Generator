import importlib

from PySide6 import QtWidgets, QtCore
from shiboken6 import wrapInstance

import maya.OpenMayaUI as omu

import procedural_forest_generator
importlib.reload(procedural_forest_generator)
from procedural_forest_generator import Tree, Forest


# Creates an instance of the GUI for the procedural forest generator
# TODO:
# Define layout & connections
class ForestGUI(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.tree_generator = Forest()
        self.setWindowTitle("Procedural Forest")
        self.create_layout()
        self.create_connections

    def create_layout(self):
        pass

    def create_connections(self):
        pass

    @QtCore.Slot()
    def create(self):
        pass