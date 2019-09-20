import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging

#
# MummyInterface
#

class MummyInterface(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "MummyInterface" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Slicelet"]
    self.parent.dependencies = []
    self.parent.contributors = ["Nayra, Guillermo, Carlos Luque"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = "Slicelet for Mummy Museam"
    self.parent.acknowledgementText = "This file was originally developed by Nayra, Guillermo, Carlos Luque " 

    #iconPath = os.path.join(os.path.dirname(self.parent.path), 'Resources/Icons', self.moduleName+'.png')
    #parent.icon = qt.QIcon(iconPath)

#
# MummyInterfaceWidget
#

class MummyInterfaceWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModuleWidget.__init__(self, parent)

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)
    
     # Show slicelet button
    showSliceletButton = qt.QPushButton("Show slicelet")
    showSliceletButton.toolTip = "Launch the slicelet"
    self.layout.addWidget(qt.QLabel(' '))
    self.layout.addWidget(showSliceletButton)
    showSliceletButton.connect('clicked()', self.launchSlicelet)
    
    # Add vertical spacer
    self.layout.addStretch(1)


  def launchSlicelet(self):
    mainFrame = SliceletMainFrame()

    #iconPath = os.path.join(os.path.dirname(slicer.modules.mummyinterface.path), 'Resources/Icons', self.moduleName+'.png')
    #mainFrame.windowIcon = qt.QIcon(iconPath)
    mainFrame.connect('destroyed()', self.onSliceletClosed)

    slicelet = MummyMuseamSlicelet(mainFrame)
    mainFrame.setSlicelet(slicelet)

    # Make the slicelet reachable from the Slicer python interactor for testing
    slicer.MummyMuseamSliceletInstance = slicelet

    return slicelet

  def onSliceletClosed(self):
    logging.debug('Slicelet closed')


class MummyInterfaceTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_MummyInterface1()


#
# MummyInterfaceLogic
#

class MummyInterfaceLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """
  def todo(self):
    pass



#
# SliceletMainFrame
#   Handles the event when the slicelet is hidden (its window closed)
#
class SliceletMainFrame(qt.QDialog):
  def setSlicelet(self, slicelet):
    self.slicelet = slicelet

  def hideEvent(self, event):
    self.slicelet.disconnect()

    import gc
    refs = gc.get_referrers(self.slicelet)
    if len(refs) > 1:
      # logging.debug('Stuck slicelet references (' + repr(len(refs)) + '):\n' + repr(refs))
      pass

    slicer.MummyInterfaceSliceletInstance = None
    self.slicelet = None
    self.deleteLater()

#
# MummyMuseamSlicelet
#

class MummyMuseamSlicelet():
  def __init__(self, FrameParent):
   
    self.frameParent = FrameParent
    self.frameParent.setLayout(qt.QVBoxLayout())

    self.layout = self.frameParent.layout()
    self.layout.setMargin(0)
    self.layout.setSpacing(0)

    uiPath = os.path.join(os.path.dirname(slicer.modules.mummyinterface.path), 'Resources/UI', 'MummyInterface.ui')

    # Load widget from .ui file (created by Qt Designer)
    uiWidget = slicer.util.loadUI(uiPath)
    self.layout.addWidget(uiWidget)
    self.ui = slicer.util.childWidgetVariables(uiWidget)

    # Add layout widget
    self.layoutWidget = slicer.qMRMLLayoutWidget()
    self.layoutWidget.setMRMLScene(slicer.mrmlScene)
    self.frameParent.layout().addWidget(self.layoutWidget)
    self.layoutWidget.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUp3DView)
    
    self.threeDWidget = self.layoutWidget.layoutManager().threeDWidget(0)
    self.threeDWidget.threeDController().setVisible(False)

    self.threeDView = self.threeDWidget.threeDView()
    self.volRenLogic = slicer.modules.volumerendering.logic()

    # set up background color, box, label axis
    self.setup3DView()

    self.setupConnections()

    #Full screen
    self.frameParent.showFullScreen() 
    self.frameParent.show()


# TODO write all connections (action)
  def setupConnections(self):
    logging.debug('Slicelet.setupConnections()')
    self.ui.mummyButton1.connect('clicked()', self.onLoadMummy1)
    self.ui.viewSButton.connect("clicked()", self.onViewSClicked)
    self.ui.viewIButton.connect("clicked()", self.onViewIClicked)

# Disconnect all connections made to the slicelet to enable the garbage collector to destruct the slicelet object on quit
  def disconnect(self):
    self.ui.mummyButton1.disconnect('clicked()', self.onLoadMummy1)
    self.ui.viewSButton.disconnect("clicked()", self.onViewSClicked)
    self.ui.viewIButton.disconnect("clicked()", self.onViewIClicked)

  def setup3DView(self):
    bg_top = 0.05, 0.05, 0.05
    bg_btm = 0.36, 0.25, 0.2
   
    viewNode = self.threeDWidget.mrmlViewNode()
    viewNode.SetBoxVisible(True)
    viewNode.SetAxisLabelsVisible(True)
    viewNode.SetBackgroundColor(bg_top)
    viewNode.SetBackgroundColor2(bg_btm)
    self.threeDView.resetCamera()

  def onLoadMummy1(self):
    logging.debug('Slicelet.onLoadMummy1()')
    slicer.mrmlScene.Clear(0)
    volumenPath = os.path.join(os.path.dirname(slicer.modules.mummyinterface.path), 'Resources/data', "CT-Chest.nrrd")

    loadedVolumeNode = slicer.util.loadVolume(volumenPath)

    if loadedVolumeNode:
      volumenNode = slicer.util.getNode('CT-Chest')
      displayNode = self.volRenLogic.CreateDefaultVolumeRenderingNodes(volumenNode)
      displayNode.SetVisibility(True)

  def onViewSClicked(self):
    self.threeDView.resetCamera()
    s_Axis = 5
    self.threeDView.rotateToViewAxis(s_Axis)


  def onViewIClicked(self):
    self.threeDView.resetCamera()
    i_Axis = 4
    self.threeDView.rotateToViewAxis(i_Axis)

    
#
# Main
#
if __name__ == "__main__":
  #TODO: access and parse command line arguments
  #   Example: SlicerRt/src/BatchProcessing
  #   Ideally handle --xml

  import sys
  logging.debug( sys.argv )

  mainFrame = qt.QFrame()
  slicelet = MummyMuseamSlicelet(mainFrame)