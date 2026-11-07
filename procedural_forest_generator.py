import importlib

import maya.cmds as cmds
from PySide6 import QtWidgets, QtCore
from shiboken6 import wrapInstance

import maya.OpenMayaUI as omu

def get_main_maya_win():
    main_win = omu.MQtUtil.mainWindow()
    return wrapInstance(int(main_win), QtWidgets.QWidget)

# TODO:
class ForestGUI(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.tree_generator = Tree()
        self.setWindowTitle("Procedural Forest")
        self.create_layout()
        self.create_connections()


    def create_layout(self):
        self.main_lay = QtWidgets.QVBoxLayout()
        self._form_ui()
        self.create_btn = QtWidgets.QPushButton("Create")
        self.main_lay.addWidget(self.create_btn)
        self.setLayout(self.main_lay)

 
    def _form_ui(self):
        self.form_layout = QtWidgets.QFormLayout()
        self.trunk_h_dspnbx = QtWidgets.QDoubleSpinBox()
        self.trunk_h_dspnbx.setValue(0.50)
        self.form_layout.addRow("Trunk Height:", self.trunk_h_dspnbx)

        self.main_lay.addLayout(self.form_layout)


    def create_connections(self):
        self.create_btn.clicked.connect(self.create)


    @QtCore.Slot()
    def create(self):
        self.tree_generator.trunk_height = self.trunk_h_dspnbx.value()
        self.tree_generator.create()


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
        self.trunk_taper_ratio = 8
        self.trunk_taper = self.trunk_width/self.trunk_taper_ratio
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
        cmds.select("trunk")
        cmds.polyMoveEdge("trunk.e[1]", translateZ=-self.trunk_taper)
        cmds.polyMoveEdge("trunk.e[2]", translateZ=self.trunk_taper)
        cmds.polyMoveEdge("trunk.e[6]", translateX=self.trunk_taper)
        cmds.polyMoveEdge("trunk.e[7]", translateX=-self.trunk_taper)

        return self.trunk_node
        

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
class Forest(Tree):

    def __init__(self):
        self.density = 0
    pass

# This class needs to:
# Create an instance of 1+ trees based on user configurations
# Pull from multiple tree types 