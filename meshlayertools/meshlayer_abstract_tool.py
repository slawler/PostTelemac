# -*- coding: utf-8 -*-

"""
/***************************************************************************
 PostTelemac
                                 A QGIS plugin
 Post Traitment or Telemac
                              -------------------
        begin                : 2015-07-07
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Artelia
        email                : patrice.Verchere@arteliagroup.com
 ***************************************************************************/
 
 ***************************************************************************/
 get Image class
 Generate a Qimage from selafin file to be displayed in map canvas 
 with tht draw method of posttelemacpluginlayer
 
Versions :
0.0 : debut

 ***************************************************************************/
"""

from __future__ import unicode_literals
#from PyQt4 import uic, QtCore, QtGui
from qgis.PyQt import uic, QtCore, QtGui
try:
    from qgis.PyQt.QtGui import QWidget, QTreeWidgetItem
except:
    from qgis.PyQt.QtWidgets import QWidget, QTreeWidgetItem
import os

#FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'ValueTool.ui'))



#class AbstractMeshLayerTool(QtGui.QWidget, FORM_CLASS):
class AbstractMeshLayerTool(QWidget):

    SOFTWARE = []

    def __init__(self, meshlayer,dialog, parent=None):
        super(AbstractMeshLayerTool, self).__init__(parent)
        #self.setupUi(self)
        self.meshlayer = meshlayer
        self.propertiesdialog = dialog
        self.widgetindex = None
        self.iconpath = None
        self.initTool()
        self.loadWidget()
        
    def initTool(self):
        """
        Load widget and icons and init things
        must contain :
            self.setupUi(self)
            self.iconpath = '...path to icon...'
        """
        pass
        
    def onActivation(self):
        pass
        
    def onDesactivation(self):
        pass
        
        
    def loadWidget(self):
        name = self.objectName()
        arb = name.split('_')
        self.qtreewidgetitem = QTreeWidgetItem()
        self.qtreewidgetitem.setText(0,arb[-1])  
        if self.iconpath != None:
            self.qtreewidgetitem.setIcon(0,QtGui.QIcon(self.iconpath))
        self.propertiesdialog.treeWidget_utils.addTopLevelItems([self.qtreewidgetitem])
        self.propertiesdialog.stackedWidget.addWidget(self)
        
        self.widgetindex = self.propertiesdialog.stackedWidget.indexOf(self)
        
        #connect signals
        self.propertiesdialog.treeWidget_utils.itemClicked.connect(self.onClickRaw)
        self.propertiesdialog.tabWidget.currentChanged.connect(self.onClickRaw)
        
    def onClickRaw(self, param1, param2 = None):
        """
        Mangage the activation of tool when tool's icon is clicked
        """
        if isinstance(param1, QTreeWidgetItem):    #signal from treeWidget_utils
            if param1 == self.qtreewidgetitem:
                self.propertiesdialog.stackedWidget.setCurrentWidget(self)
                self.onActivation()
            else:
                self.onDesactivation()
        elif isinstance(param1, int):                  #signal from tabWidget
            if self.propertiesdialog.tabWidget.widget(param1).objectName() == 'Toolstab':
                if self.propertiesdialog.treeWidget_utils.currentItem() == self.qtreewidgetitem:
                    self.onActivation()
            else:
                self.onDesactivation()
                

        

            
        
        
        
        

        
        
        