import maya.cmds as cmds
from PySide6 import QtWidgets, QtCore
# TODO:
# Fix 'Import "maya.cmds" could not be resolved.'


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


# Creates an instance of a tree 
# TODO: 
# Add at least 2 tree types
# Figure out how to do that ^ lol (Tree type classes that inhereit Tree?)
# Maybe create "tree age" quality that sets a range of avg tree sizes
# Allows user to decide tree size without picking numbers idk
# Define create functions
class Tree():

    def __init__(self):
        self.trunk_height = 2.5
        self.trunk_width = .25
        self.canopy_height = 2
        self.canopy_width = 2
        self.grp_name = "myTree"


    def create(self):
        group_objs = []
        group_objs.append(self.create_trunk())
        group_objs.append(self.create_canopy())
        cmds.group(group_objs, name=self.grp_name)


    def create_trunk(self):
        self.trunk_obj, self.trunk_node = cmds.polyCube(name="trunk",height=self.trunk_height
                        ,width=self.trunk_width, depth=self.trunk_width)
        cmds.xform(self.trunk_obj, pivots=[0, -self.trunk_height/2.0,0])
        cmds.xform(translation=[0,self.trunk_height/2.0,0])
        return self.trunk_obj
        

    def create_canopy(self):
        self.canopy_obj, self.canopy_node = cmds.polyCube(name="canopy",height=self.canopy_height
                        ,width=self.canopy_width, depth=self.canopy_width)
        cmds.xform(translation=[0,self.trunk_height,0])
        return self.canopy_obj
        # Create canopy with polyCone, polyCube, etc
        # Shape based on tree type
        # Oak = polySphere or polyCube
        # Pine = polyCone or tapered polyCube


# Creates an instance of a forest
# Creates # of trees based on density attributes & forest size
# TODO:
# Research how to define tree placement/density to Maya
# Find way to define forest size by drawing a path?? (challenging feature)
class Forest():

    def __init__(self):
        self.density = 0
    pass