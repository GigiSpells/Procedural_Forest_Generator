import importlib
import random

import maya.cmds as cmds
from PySide6 import QtWidgets, QtCore
from shiboken6 import wrapInstance

#import maya.OpenMayaUI as omu

#def get_main_maya_win():
    #main_win = omu.MQtUtil.mainWindow()
    #return wrapInstance(int(main_win), QtWidgets.QWidget)

# ForestGUI() TODO:
 # modify _form_ui() to modify Forest() attributes
 # use trunk & canopy size ranges for tree variety

class ForestGUI(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.tree_gen = Tree()
        self.forest_gen = Forest()
        self.setWindowTitle("Forest Generator")
        self.resize(300,200)
        self.create_layout()
        self.create_connections()


    def create_layout(self):
        self.main_lay = QtWidgets.QVBoxLayout()
        self._form_ui()
        self.create_btn = QtWidgets.QPushButton("Create")
        self.main_lay.addWidget(self.create_btn)
        self.setLayout(self.main_lay)


    def _set_trunk_parameters(self):

        self.trunk_h_min = QtWidgets.QDoubleSpinBox()
        self.trunk_h_min.setRange(0.1, 10.0)
        self.trunk_h_min.setDecimals(2)
        self.trunk_h_min.setSingleStep(0.1)
        self.trunk_h_min.setValue(2.0)

        self.trunk_h_max = QtWidgets.QDoubleSpinBox()
        self.trunk_h_max.setRange(0.1, 10.0)
        self.trunk_h_max.setDecimals(2)
        self.trunk_h_max.setSingleStep(0.1)
        self.trunk_h_max.setValue(3.0)


        self.trunk_w_min = QtWidgets.QDoubleSpinBox()
        self.trunk_w_min.setRange(0.1, 10.0)
        self.trunk_w_min.setDecimals(2)
        self.trunk_w_min.setSingleStep(0.1)
        self.trunk_w_min.setValue(2.0)

        self.trunk_w_max = QtWidgets.QDoubleSpinBox()
        self.trunk_w_max.setRange(0.1, 10.0)
        self.trunk_w_max.setDecimals(2)
        self.trunk_w_max.setSingleStep(0.1)
        self.trunk_w_max.setValue(3.0)


    def _set_canopy_parameters(self):

        self.canopy_h_min = QtWidgets.QDoubleSpinBox()
        self.canopy_h_min.setRange(0.1, 10.0)
        self.canopy_h_min.setDecimals(2)
        self.canopy_h_min.setSingleStep(0.1)
        self.canopy_h_min.setValue(2.0)

        self.canopy_h_max = QtWidgets.QDoubleSpinBox()
        self.canopy_h_max.setRange(0.1, 10.0)
        self.canopy_h_max.setDecimals(2)
        self.canopy_h_max.setSingleStep(0.1)
        self.canopy_h_max.setValue(3.0)

        self.canopy_w_min = QtWidgets.QDoubleSpinBox()
        self.canopy_w_min.setRange(0.1, 10.0)
        self.canopy_w_min.setDecimals(2)
        self.canopy_w_min.setSingleStep(0.1)
        self.canopy_w_min.setValue(2.0)

        self.canopy_w_max = QtWidgets.QDoubleSpinBox()
        self.canopy_w_max.setRange(0.1, 10.0)
        self.canopy_w_max.setDecimals(2)
        self.canopy_w_max.setSingleStep(0.1)
        self.canopy_w_max.setValue(3.0)


    def _form_ui(self):

        self._set_trunk_parameters()
        self._set_canopy_parameters()

        self.form_layout = QtWidgets.QFormLayout()

        #Add connection
        self.forest_type_cmbobx = QtWidgets.QComboBox()
        self.forest_type_cmbobx.addItems(["Oak","Pine","Mixed"])
        self.form_layout.addRow("Forest Type:", self.forest_type_cmbobx)

        self.size_cmbobx = QtWidgets.QComboBox()
        self.size_cmbobx.addItems(["Small","Medium","Large"])
        self.form_layout.addRow("Size:", self.size_cmbobx)

        self.density_cmbobx = QtWidgets.QComboBox()
        self.density_cmbobx.addItems(["Sparse","Average","Dense"])
        self.form_layout.addRow("Density:", self.density_cmbobx)

        self.form_layout.addRow("Trunk Height Min:", self.trunk_h_min)
        self.form_layout.addRow("Trunk Height Max:", self.trunk_h_max)

        self.form_layout.addRow("Trunk Width Min:", self.trunk_w_min)
        self.form_layout.addRow("Trunk Width Max:", self.trunk_w_max)

        self.form_layout.addRow("Canopy Height Min:", self.canopy_h_min)
        self.form_layout.addRow("Canopy Height Max:", self.canopy_h_max)

        self.form_layout.addRow("Canopy Width Min:", self.canopy_w_min)
        self.form_layout.addRow("Canopy Width Max:", self.canopy_w_max)

        self.grp_name_le = QtWidgets.QLineEdit()
        self.grp_name_le.setText(self.tree_gen.grp_name)
        self.form_layout.addRow("Group Name:", self.grp_name_le)

        self.main_lay.addLayout(self.form_layout)


    def create_connections(self):
        self.create_btn.clicked.connect(self.create)


    @QtCore.Slot()
    def create(self):
        self.forest_gen.type = self.forest_type_cmbobx.currentText()
        self.forest_gen.size = self.size_cmbobx.currentText()
        self.forest_gen.density = self.density_cmbobx.currentText()
        
        self.forest_gen.create()


class Tree():

    def __init__(self, type="Oak"):
        self.tree_types = ["Oak", "Pine"]
        self.type = type
        self.trunk_height = 2.5
        self.trunk_width = .25
        self.trunk_taper_ratio = 8
        self.trunk_taper = self.trunk_width/self.trunk_taper_ratio
        self.canopy_height = 2
        self.canopy_width = 2
        self.grp_name = "myTree"


    def create(self):
        objects = []
        objects.append(self.create_trunk())
        objects.append(self.define_tree_type())
        return cmds.group(objects, name=self.grp_name)


    def create_trunk(self):
        self.trunk_obj, self.trunk_node = cmds.polyCube(name="trunk",height=self.trunk_height
                        ,width=self.trunk_width, depth=self.trunk_width)
        cmds.xform(self.trunk_obj, pivots=[0, -self.trunk_height/2.0,0])
        cmds.xform(self.trunk_obj, translation=[0,self.trunk_height/2.0,0])
        
        cmds.polyMoveEdge(f"{self.trunk_obj}.e[1]", translateZ=-self.trunk_taper)
        cmds.polyMoveEdge(f"{self.trunk_obj}.e[2]", translateZ=self.trunk_taper)
        cmds.polyMoveEdge(f"{self.trunk_obj}.e[6]", translateX=self.trunk_taper)
        cmds.polyMoveEdge(f"{self.trunk_obj}.e[7]", translateX=-self.trunk_taper)

        return self.trunk_obj
        

    def create_oak_canopy(self):
        self.canopy_obj, self.canopy_node = cmds.polyCube(name="canopy",height=self.canopy_height
                        ,width=self.canopy_width, depth=self.canopy_width)
        cmds.xform(self.canopy_obj, pivots=[0, -self.canopy_height/2.0,0])
        cmds.xform(translation=[0,self.trunk_height,0])
        cmds.xform(self.canopy_obj, translation=[0,self.trunk_height,0])
        
        # self.canopy2_obj = cmds.duplicate(self.canopy_obj, name="canopy2")
        # cmds.xform(self.canopy2_obj, translation=[5,0,0])
        # cmds.xform(translation=[0,self.trunk_height,0])

        return self.canopy_obj
        # self.canopy_grp = cmds.group(self.canopy_obj,self.canopy2_obj, name="canopy_GRP")
        # return self.canopy_grp


    def create_pine_canopy(self):
        self.canopy_obj, self.canopy_node = cmds.polyCube(name="canopy",height=self.canopy_height
                        ,width=self.canopy_width, depth=self.canopy_width)
        cmds.xform(self.canopy_obj, pivots=[0, -self.canopy_height/2.0,0])
        cmds.xform(translation=[0,self.trunk_height,0])
        cmds.polyMoveEdge(f"{self.canopy_obj}.e[1]", translateZ=-self.canopy_width/4)
        cmds.polyMoveEdge(f"{self.canopy_obj}.e[2]", translateZ=self.canopy_width/4)
        cmds.polyMoveEdge(f"{self.canopy_obj}.e[6]", translateX=self.canopy_width/4)
        cmds.polyMoveEdge(f"{self.canopy_obj}.e[7]", translateX=-self.canopy_width/4)

        self.canopy2_obj = cmds.duplicate(self.canopy_obj, name="canopy2")
        cmds.xform(self.canopy2_obj, translation=[0,self.canopy_height*1.6,0])

        self.canopy_grp = cmds.group(self.canopy_obj,self.canopy2_obj, name="canopy_GRP")
        return self.canopy_grp


    def define_tree_type(self):
        if self.type == "Mixed":
            self.type = random.choice(self.tree_types)
        elif self.type == "Oak":
            return self.create_oak_canopy()
        elif self.type == "Pine":
            return self.create_pine_canopy()

# Forest() TODO:
# Coordinate with ForestGUI()

class Forest():

    def __init__(self):
        self.type = "Oak"
        self.tree_types = ["Oak", "Pine"]
        self.area_size = {
            "Small": 50.0,
            "Medium": 100.0,
            "Large": 150.0,
        }
        self.min_spacing = {
            "Sparse": 20.0,
            "Average": 11.25,
            "Dense": 6.25
        }
        self.size = "Small"
        self.density = "Average"
        self.trunk_height_range = 0
        self.trunk_width_range = 0
        self.canopy_height_range = 0
        self.canopy_width_range = 0
        self.trees = []


    def create_trees(self):
        area = self.area_size[self.size]
        min_spacing = self.min_spacing[self.density]

        target_count = max(1, int((area / min_spacing) ** 2 * 0.5))

        positions = self._get_random_pos(
            count = target_count,
            area = area,
            min_spacing = min_spacing
        )

        for i, (x, z) in enumerate(positions):
            tree_type = (
                random.choice(self.tree_types)
                if self.type == "Mixed"
                else self.type
            )

            tree = Tree(tree_type)
            tree.grp_name = f"tree{i + 1}"
            group_name = tree.create()

            cmds.xform(group_name, translation=[x, 0, z])
            self.trees.append(group_name)

        self.forest_grp = cmds.group(self.trees, name="Forest_GRP")

        return self.trees


    def _get_random_pos(self, count, area, min_spacing):
        positions = []
        half = area / 2
        min_spacing_sq = min_spacing ** 2

        while len(positions) < count:

            x = random.uniform(-half, half)
            z = random.uniform(-half, half)

            far_enough = all(
                (x - px) ** 2 + (z - pz) ** 2 >= min_spacing_sq
                for px, pz in positions
            )

            if far_enough:
                positions.append((x,z))

        return positions


    def create(self):
        self.create_trees()