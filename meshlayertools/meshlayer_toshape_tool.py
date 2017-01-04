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


from PyQt4 import uic, QtCore, QtGui
from meshlayer_abstract_tool import *
import os
import qgis

from toshape.posttelemac_util_extractshp import *
from toshape.posttelemac_util_extractmesh import *
from toshape.posttelemac_util_extractpts import *


FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'ToshapeTool.ui'))



class ToShapeTool(AbstractMeshLayerTool,FORM_CLASS):


    def __init__(self, meshlayer,dialog):
        AbstractMeshLayerTool.__init__(self,meshlayer,dialog)
        
    def initTool(self):
        self.setupUi(self)
        self.iconpath = os.path.join(os.path.dirname(__file__),'..','icons','tools','layer_add.png' )
        
        self.checkBox_contourcrs.stateChanged.connect(self.enablecheckbox)
        self.pushButton_contourcrs.clicked.connect(self.set_utilcrs)
        self.pushButton_contourcreate.clicked.connect(self.create_shp)
        #2shape mesh
        self.checkBox_3.stateChanged.connect(self.enablecheckbox)
        #self.checkBox_2.stateChanged.connect(self.enablecheckbox)
        #self.pushButton_7.clicked.connect(self.set_utilcrs)
        self.pushButton_10.clicked.connect(self.create_shp_maillage)
        #2shape  Points
        #self.checkBox_4.stateChanged.connect(self.enablecheckbox)
        self.checkBox_5.stateChanged.connect(self.enablecheckbox)
        #self.pushButton_9.clicked.connect(self.set_utilcrs)
        self.pushButton_2.clicked.connect(self.create_shp_points)
        

        
    def onActivation(self):
        pass

    def onDesactivation(self):
        pass
        
        
        
    def enablecheckbox(self,int1):
        """
        Enable checkboxes for activating buttons when another buttons are activated
        """
        source = self.sender()
        if source == self.checkBox_contourcrs:
            if int1 == 2:
                self.pushButton_contourcrs.setEnabled(True)
            elif int1 == 0:
                self.pushButton_contourcrs.setEnabled(False)
        if source == self.checkBox_3:
            if int1 == 2:
                self.doubleSpinBox.setEnabled(True)
                self.doubleSpinBox_2.setEnabled(True)
                self.doubleSpinBox_3.setEnabled(True)
            elif int1 == 0:
                self.doubleSpinBox.setEnabled(False)
                self.doubleSpinBox_2.setEnabled(False)
                self.doubleSpinBox_3.setEnabled(False)

                
    def set_utilcrs(self):
        self.crsselector.exec_()
        crs = self.crsselector.selectedAuthId()
        source = self.sender()
        #print str(source.name())
        """
        if source == self.pushButton_crs:
            self.label_selafin_crs.setText(crs)
        else:
            source.setText(crs)
        """
        source.setText(crs)
            
            
    def create_shp_maillage(self):
        """
        Called when Shape / create mesh is activated
        """
        self.create_shp_maillage()

    def create_shp(self):
        """
        Called when Shape / create contour is activated
        """
        self.create_shp()
        
    def create_shp_points(self):
        """
        Called when Shape / create points is activated
        """
        self.create_points()
        
        
    def create_points(self):
        self.initclass=InitSelafinMesh2Pts()
        self.initclass.status.connect(self.propertiesdialog.textBrowser_2.append)
        self.initclass.finished1.connect(self.workershapePointFinished)
        self.initclass.start(                 
                             0,                 #0 : thread inside qgis (plugin) - 1 : thread processing - 2 : modeler (no thread) - 3 : modeler + shpouput - 4: outsideqgis
                             os.path.normpath(self.meshlayer.hydraufilepath),                 #path to selafin file
                             self.meshlayer.time_displayed,                            #time to process (selafin time in interation if int, or second if str)
                             self.spinBox.value(),                     #space step
                             self.checkBox_5.isChecked(),               #bool for comuting velocity
                             self.meshlayer.hydrauparser.parametrevx if self.checkBox_5.isChecked() else None,
                             self.meshlayer.hydrauparser.parametrevy if self.checkBox_5.isChecked() else None,
                             #[self.selafinlayer.hydrauparser.getValues(self.selafinlayer.time_displayed)[i] for i in range(len([param for param in self.selafinlayer.hydrauparser.parametres if not param[2]]))],                          #tab of values
                             [self.meshlayer.hydrauparser.getValues(self.meshlayer.time_displayed)[i] for i in range(len([param for param in self.meshlayer.hydrauparser.parametres]))],                          #tab of values
                             self.meshlayer.crs().authid(),      #selafin crs
                             translatex = self.meshlayer.hydrauparser.translatex,
                             translatey = self.meshlayer.hydrauparser.translatey,
                             selafintransformedcrs = None,   #if no none, specify crs of output file
                             outputshpname = None,           #change generic outputname to specific one
                             outputshppath = None,         #if not none, create shp in this directory
                             outputprocessing = None)    #needed for toolbox processing
                             
                             

    def create_shp(self):
        self.initclass=InitSelafinContour2Shp()
        self.initclass.status.connect(self.propertiesdialog.textBrowser_2.append)
        self.initclass.error.connect(self.propertiesdialog.textBrowser_2.append)
        self.initclass.finished1.connect(self.workershapeFinished)
        self.propertiesdialog.normalMessage(self.tr("2Shape - coutour creation launched - watch progress on log tab"))
        
        if  self.lineEdit_contourname.text() == "":
            """
            name = (str(self.selafinlayer.hydrauparser.parametres[self.selafinlayer.param_displayed][1]).translate(None, "?,!.;")
                             +"_t_"+str(int(self.selafinlayer.time_displayed)) )
            """
            name = ( self.meshlayer.hydrauparser.parametres[self.meshlayer.param_displayed][1]
                             + "_t_" + str(int(self.meshlayer.time_displayed)) )
            
        else:
            name = self.lineEdit_contourname.text()
        
        self.initclass.start(0,                 #0 : thread inside qgis (plugin) - 1 : thread processing - 2 : modeler (no thread) - 3 : modeler + shpouput - 4: outsideqgis
                         os.path.normpath(self.meshlayer.hydraufilepath),                 #path to selafin file
                         int(self.meshlayer.time_displayed),                            #time to process (selafin time iteration)
                         self.meshlayer.hydrauparser.parametres[self.meshlayer.param_displayed][1],                     #parameter to process name (string) or id (int)
                         self.meshlayer.meshrenderer.lvl_contour,                       #levels to create
                         self.meshlayer.crs().authid(),      #selafin crs
                         translatex = self.meshlayer.hydrauparser.translatex,
                         translatey = self.meshlayer.hydrauparser.translatey,
                         selafintransformedcrs = self.pushButton_contourcrs.text() if self.checkBox_contourcrs.isChecked() else None,   #if no none, specify crs of output file
                         quickprocessing = False,                #quickprocess option - don't make ring
                          outputshpname = name,           #change generic outputname to specific one
                         outputshppath = None,         #if not none, create shp in this directory
                         forcedvalue = self.meshlayer.value,          #force value for plugin
                         outputprocessing = None)
        

            
    def create_shp_maillage(self):
        self.initclass=InitSelafinMesh2Shp()
        self.initclass.status.connect(self.propertiesdialog.textBrowser_2.append)
        if self.checkBox_3.isChecked():
            self.initclass.finished1.connect(self.workerFinishedHillshade)
        else:
            self.initclass.finished1.connect(self.workershapeFinished)
        self.propertiesdialog.normalMessage(self.tr("2Shape - mesh creation launched - watch progress on log tab"))
        self.initclass.start(0,                 #0 : thread inside qgis (plugin) - 1 : thread processing - 2 : modeler (no thread) - 3 : modeler + shpouput - 4: outsideqgis
                         os.path.normpath(self.meshlayer.hydraufilepath),                 #path to selafin file
                         int(self.meshlayer.time_displayed),                            #time to process (selafin time iteration)
                         #parameter = str(self.getParameterName('BATHYMETRIE')[0]) if self.checkBox_3.isChecked() else None,     #parameter to process name (string) or id (int)
                         parameter =  str(  self.meshlayer.hydrauparser.parametres[self.meshlayer.hydrauparser.parambottom][1]   )   if self.checkBox_3.isChecked() else None,
                         facteurz = self.doubleSpinBox.value(),                 #z amplify
                         azimuth = self.doubleSpinBox_3.value(),                    #azimuth for hillshade
                         zenith = self.doubleSpinBox_2.value(),                    #zenith for hillshade
                         selafincrs = self.meshlayer.crs().authid(),      #selafin crs
                         translatex = self.meshlayer.hydrauparser.translatex,
                         translatey = self.meshlayer.hydrauparser.translatey,
                         selafintransformedcrs = self.pushButton_contourcrs.text() if self.checkBox_contourcrs.isChecked() else None,   #if no none, specify crs of output file
                         outputshpname = None,           #change generic outputname to specific one
                         outputshppath = None,         #if not none, create shp in this directory
                         outputprocessing = None)
            
            
    def workershapeFinished(self,strpath):
        vlayer = qgis.core.QgsVectorLayer( strpath, os.path.basename(strpath).split('.')[0],"ogr")
        qgis.core.QgsMapLayerRegistry.instance().addMapLayer(vlayer)
        #self.selafinlayer.propertiesdialog.textBrowser_main.append(ctime() + " - "+ str(os.path.basename(strpath).split('.')[0]) + self.tr(" created"))
        self.propertiesdialog.normalMessage(str(os.path.basename(strpath).split('.')[0]) + self.tr(" created"))
        
    def workershapePointFinished(self,strpath):
        vlayer = qgis.core.QgsVectorLayer( strpath, os.path.basename(strpath).split('.')[0],"ogr")
        if self.checkBox_5.isChecked():
            pathpointvelocityqml = os.path.join(os.path.dirname(__file__), '..','styles', '00_Points_Vmax_vecteur_champ_vectoriel.qml')
            vlayer.loadNamedStyle(pathpointvelocityqml)
        qgis.core.QgsMapLayerRegistry.instance().addMapLayer(vlayer)
        #self.selafinlayer.propertiesdialog.textBrowser_main.append(ctime() + " - "+ str(os.path.basename(strpath).split('.')[0]) + self.tr(" created"))
        self.propertiesdialog.normalMessage(str(os.path.basename(strpath).split('.')[0]) + self.tr(" created"))
        

    def workerFinishedHillshade(self,strpath):
        vlayer = qgis.core.QgsVectorLayer( strpath, os.path.basename(strpath).split('.')[0],"ogr")
        pathhillshadeqml = os.path.join(os.path.dirname(__file__), '..','styles', '00_Polygon_Hillshade.qml')
        vlayer.loadNamedStyle(pathhillshadeqml)
        qgis.core.QgsMapLayerRegistry.instance().addMapLayer(vlayer)
        #self.selafinlayer.propertiesdialog.textBrowser_main.append(ctime() + " - "+ str(os.path.basename(strpath).split('.')[0]) + self.tr(" created"))
        self.propertiesdialog.normalMessage(str(os.path.basename(strpath).split('.')[0]) + self.tr(" created"))
