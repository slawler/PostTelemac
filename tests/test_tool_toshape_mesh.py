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
import sys
import os

from  PostTelemac.meshlayer.post_telemac_pluginlayer import SelafinPluginLayer
from PostTelemac.meshlayertools.meshlayer_toshape_tool import ToShapeTool



def testToshapeTool():
    
    print('begin')
    path = os.path.normpath('C://00_Bureau//data2//SMEAG_REF_Q100.res')
    slf = SelafinPluginLayer()
    print('slf created')
    slf.load_selafin(path,'TELEMAC')
    print('slf loaded')
    
    slf.propertiesdialog.debugtoprint = True
    
    shapetool = ToShapeTool(slf,slf.propertiesdialog)
    shapetool.checkBox_3.setCheckState(2)   #for hillshade rendering
    
    print('param1',str(  shapetool.meshlayer.hydrauparser.parametres[shapetool.meshlayer.hydrauparser.parambottom][1]   ))
    
    shapetool.create_shp_maillage()
    
    print('done')
    
    
testToshapeTool()
    
            
        

    
    
    
