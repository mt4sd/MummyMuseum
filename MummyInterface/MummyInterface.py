import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging

#
# MummyInterfacePresets
#
class MummyInterfacePresets():
  INSIDE = "InsidePreset"
  OUTSIDE = "OutsidePreset"

class MummyInterfaceViews():
  LEFT = 0
  RIGHT = 1
  POSTERIOR = 2
  ANTERIOR = 3
  INFERIOR = 4
  SUPERIOR = 5
  
class MummyInterfaceDataset():
  MUMMY1 = {"name": "Mummy1", "dataFilename": "Mummy1.nrrd", "descriptionFilename" : "Mummy1.txt"}
  MUMMY2 = {"name": "Mummy2", "dataFilename": "Mummy2.nrrd", "descriptionFilename" : "Mummy2.txt"}
  MUMMY3 = {"name": "Mummy3", "dataFilename": "Mummy3.nrrd", "descriptionFilename" : "Mummy3.txt"}

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
    self.parent.dependencies = ["VolumeRendering", "VirtualReality"]
    self.parent.contributors = ["Nayra, Guillermo, Carlos Luque, Abian Hernandez"] # replace with "Firstname Lastname (Organization)"
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
    self.logic = MummyInterfaceLogic()

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    layoutManager = slicer.app.layoutManager()
    layoutManager.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUp3DView)
    layoutManager.threeDWidget(0).threeDController().setVisible(False)
    self.setup3DView(layoutManager)


    moduleDir = os.path.dirname(__file__)
    uiPath = os.path.join(moduleDir, 'Resources', 'UI', 'MummyInterface.ui')
    # Load widget from .ui file (created by Qt Designer)
    self.ui = slicer.util.loadUI(uiPath)
    self.layout.addWidget(self.ui)

    self.setupConnections()


  def setup3DView(self, layoutManager):
    viewNode = layoutManager.threeDWidget(0).mrmlViewNode()
    viewNode.SetBoxVisible(False)
    viewNode.SetAxisLabelsVisible(False)
    self.logic.setDefaultBackgroundColor(viewNode)


  def setupConnections(self):
    logging.debug('Slicelet.setupConnections()')
    self.ui.mummyButton1.clicked.connect(lambda: self.onLoadMummy(MummyInterfaceDataset.MUMMY1))
    self.ui.mummyButton2.clicked.connect(lambda: self.onLoadMummy(MummyInterfaceDataset.MUMMY2))
    self.ui.mummyButton3.clicked.connect(lambda: self.onLoadMummy(MummyInterfaceDataset.MUMMY3))
    self.ui.viewButtonS.toggled.connect(lambda: self.onViewClicked(self.ui.viewButtonS))
    self.ui.viewButtonI.toggled.connect(lambda: self.onViewClicked(self.ui.viewButtonI))
    self.ui.viewButtonA.toggled.connect(lambda: self.onViewClicked(self.ui.viewButtonA))
    self.ui.viewButtonP.toggled.connect(lambda: self.onViewClicked(self.ui.viewButtonP))
    self.ui.viewButtonL.toggled.connect(lambda: self.onViewClicked(self.ui.viewButtonL))
    self.ui.viewButtonR.toggled.connect(lambda: self.onViewClicked(self.ui.viewButtonR))
    self.ui.volumeRenderingAButton.clicked.connect(lambda: self.logic.activatePreset(MummyInterfacePresets.OUTSIDE))
    self.ui.volumeRenderingBButton.clicked.connect(lambda: self.logic.activatePreset(MummyInterfacePresets.INSIDE))
    self.ui.vrActivationButton.clicked.connect(lambda: self.onSwitchVirtualRealityActivation())

  def onViewClicked(self, viewbutton):
    if viewbutton.text == "Superior":
      self.logic.setViewAxis(MummyInterfaceViews.SUPERIOR)
    if viewbutton.text == "Inferior":
      self.logic.setViewAxis(MummyInterfaceViews.INFERIOR)
    if viewbutton.text == "Frontal":
      self.logic.setViewAxis(MummyInterfaceViews.ANTERIOR)
    if viewbutton.text == "Trasera":
      self.logic.setViewAxis(MummyInterfaceViews.POSTERIOR)
    if viewbutton.text == "Izquierda":
      self.logic.setViewAxis(MummyInterfaceViews.LEFT)
    if viewbutton.text == "Derecha":
      self.logic.setViewAxis(MummyInterfaceViews.RIGHT)

  def onLoadMummy(self, mummyDataset):
    self.logic.loadMummy(mummyDataset)
    self.setup3DView(slicer.app.layoutManager())
    description = self.logic.loadMummyDescription(mummyDataset)
    self.ui.explanatoryText.setPlainText(description)

  # Disconnect all connections made to the slicelet to enable the garbage collector to destruct the slicelet object on quit
  def disconnect(self):
    self.ui.mummyButton1.clicked.disconnect(self.onLoadMummy())
    self.ui.mummyButton2.clicked.disconnect(self.onLoadMummy())
    self.ui.mummyButton3.clicked.disconnect(self.onLoadMummy())
    self.ui.viewButtonS.toggled.disconnect(lambda: self.onViewClicked())
    self.ui.viewButtonI.toggled.disconnect(lambda: self.onViewClicked())
    self.ui.viewButtonA.toggled.disconnect(lambda: self.onViewClicked())
    self.ui.viewButtonP.toggled.disconnect(lambda: self.onViewClicked())
    self.ui.viewButtonL.toggled.disconnect(lambda: self.onViewClicked())
    self.ui.viewButtonR.toggled.disconnect(lambda: self.onViewClicked())
    self.ui.volumeRenderingAButton.clicked.disconnect(lambda: self.logic.activatePreset())
    self.ui.volumeRenderingBButton.clicked.disconnect(lambda: self.logic.activatePreset())
    self.ui.vrActivationButton.clicked.disconnect(lambda: self.onSwitchVirtualRealityActivation())
    
  def onSwitchVirtualRealityActivation(self):
    if (self.logic.vrEnabled):
      self.logic.deactivateVirtualReality()
      self.ui.vrActivationButton.setText("Activar RV")
      self.ui.vrResetButton.setEnabled(False)
    else:
      self.logic.activateVirtualReality()
      self.ui.vrActivationButton.setText("Desactivar RV")
      self.ui.vrResetButton.setEnabled(True)
      slicer.modules.virtualreality.viewWidget().updateViewFromReferenceViewCamera()

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

  def __init__(self):
    self.currentMummyDataset = None
    self.volumeRendDisplayNode = None
    self.vrEnabled = False
    self.threeDView = slicer.app.layoutManager().threeDWidget(0).threeDView()
    self.volRenLogic = slicer.modules.volumerendering.logic()
    self.vrLogic = slicer.modules.virtualreality.logic()
    self.setupCustomPreset()


    # Set the Default rendering method. They can be:
    #    - vtkMRMLCPURayCastVolumeRenderingDisplayNode (combobox: "VTK CPU Ray Casting" )
    #    - vtkMRMLGPURayCastVolumeRenderingDisplayNode (combobox: "VTK GPU Ray Casting" )
    #    - vtkMRMLMultiVolumeRenderingDisplayNode (combobox: "VTK Multi-Volume" )
    self.volRenLogic.SetDefaultRenderingMethod("vtkMRMLGPURayCastVolumeRenderingDisplayNode")
    
  def loadMummy(self, mummyDataset):
    logging.debug('Slicelet.onLoadMummy()')

    # clean all generated node in mrml
    slicer.mrmlScene.Clear(0)
    #self.setup3DView()
    self.currentMummyDataset = mummyDataset

    moduleDir = os.path.dirname(__file__)
    volumenPath = os.path.join(moduleDir, 'Resources', 'Data', mummyDataset["dataFilename"])
    loadedVolumeNode = slicer.util.loadVolume(volumenPath)

    if loadedVolumeNode:
      volumeNode = slicer.util.getNode(mummyDataset["name"])
      if volumeNode:
        self.currentMummyDataset = mummyDataset
        # Create all nodes and associated with VolumeNode
        self.volumeRendDisplayNode = self.volRenLogic.CreateDefaultVolumeRenderingNodes(volumeNode)
        # Setup the outside preset
        self.activatePreset(MummyInterfacePresets.OUTSIDE)
        self.volumeRendDisplayNode.SetVisibility(True)
      else:
        logging.debug('Slicelet.onLoadMummyX(): No found the mummy node' + mummyDataset["name"])
    else:
        logging.debug('Slicelet.onLoadMummyX(): No load the mummy' + mummyDataset["name"])

  def setupCustomPreset(self):
    moduleDir = os.path.dirname(__file__)
    presetsScenePath = os.path.join(moduleDir, 'Resources', 'VolRen', 'MyPresets.mrml')

    # Read presets scene
    mrmlScene = slicer.vtkMRMLScene()
    vrPropNode = slicer.vtkMRMLVolumePropertyNode()
    mrmlScene.RegisterNodeClass(vrPropNode)
    mrmlScene.SetURL(presetsScenePath)
    mrmlScene.Connect()

    # Add presets to volume rendering logic
    vrNodes = mrmlScene.GetNodesByClass("vtkMRMLVolumePropertyNode")
    vrNodes.UnRegister(None)
    for itemNum in range(vrNodes.GetNumberOfItems()):
      node = vrNodes.GetItemAsObject(itemNum)
      self.volRenLogic.AddPreset(node)

  def activatePreset(self, PresetName):
    if self.currentMummyDataset == None:
      return
    
    volumeNode = slicer.util.getNode(self.currentMummyDataset['name'])
    
    if volumeNode:
      # Get the (Volumen Rendering) display node associated with the volume node
      displayNode = self.volRenLogic.GetFirstVolumeRenderingDisplayNode(volumeNode)
      # Copy the presert to a current displayNode
      displayNode.GetVolumePropertyNode().Copy(self.volRenLogic.GetPresetByName(PresetName))
    else:
      logging.debug('Slicelet.activatePreset(): No found the mummy node' + self.currentMummyName)

  def setDefaultBackgroundColor(self, viewNode):
    bg_top = 0.05, 0.05, 0.05
    bg_btm = 0.36, 0.25, 0.2
    viewNode.SetBackgroundColor(bg_top)
    viewNode.SetBackgroundColor2(bg_btm)

  def activateVirtualReality(self):
    if (self.vrEnabled):
      return
    self.vrLogic.SetVirtualRealityConnected(True)
    vrViewNode = self.vrLogic.GetVirtualRealityViewNode()
    vrViewNode.SetLighthouseModelsVisible(False)
    self.volumeRendDisplayNode.AddViewNodeID(vrViewNode.GetID())
    self.setDefaultBackgroundColor(vrViewNode)
    self.vrLogic.SetVirtualRealityActive(True)
    self.vrEnabled = True

  def deactivateVirtualReality(self):
    if (not self.vrEnabled):
      return
    self.vrLogic.SetVirtualRealityConnected(False)
    self.vrLogic.SetVirtualRealityActive(False)
    self.vrEnabled = False
  
  def loadMummyDescription(self, mummyDataset):
    moduleDir = os.path.dirname(__file__)
    descriptionPath = os.path.join(moduleDir, 'Resources', 'Data', mummyDataset["descriptionFilename"])

    descriptionFile = open(descriptionPath, "r")
    if (descriptionFile.mode == 'r'):
      description = descriptionFile.read()
    descriptionFile.close()
    return description

  def rotate(self, axis, degree):
    print("TODO")

  def setViewAxis(self, viewAxis):
    # Set a VTK predefined view axis
    self.threeDView.resetCamera()
    self.threeDView.rotateToViewAxis(viewAxis)

    # Set the attitude customized to the presentation of the mummies
    if (viewAxis == MummyInterfaceViews.LEFT):
      for step in range(18):
        self.threeDView.roll()
    if (viewAxis == MummyInterfaceViews.RIGHT):
      for step in range(54):
        self.threeDView.roll()
    if (viewAxis == MummyInterfaceViews.SUPERIOR):
      for step in range(36):
        self.threeDView.roll()
    self.threeDView.resetFocalPoint()

  ###############
 ## To Remove ##
###############
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

    self.currentMummyName = ""
    self.currentExplanation = ""
   
    self.frameParent = FrameParent
    self.frameParent.setLayout(qt.QHBoxLayout())

    self.logic = MummyInterfaceLogic()

    self.layout = self.frameParent.layout()
    self.layout.setMargin(0)
    self.layout.setSpacing(0)

    moduleDir = os.path.dirname(__file__)
    uiPath = os.path.join(moduleDir, 'Resources', 'UI', 'MummyInterface.ui')

    # Load widget from .ui file (created by Qt Designer)
    self.uiWidget = slicer.util.loadUI(uiPath)
    self.layout.addWidget(self.uiWidget)
    self.ui = slicer.util.childWidgetVariables(self.uiWidget)

    # keyboard "v" shows the control panel
    shortcutShow = qt.QShortcut(self.frameParent)
    shortcutShow.setKey(qt.QKeySequence("v"))
    shortcutShow.connect('activated()', lambda: self.showPanel())

    # keyboard "e" hides the control panel
    shortcutHide = qt.QShortcut(self.frameParent)
    shortcutHide.setKey(qt.QKeySequence("e"))
    shortcutHide.connect('activated()', lambda: self.hidePanel())

    # Add layout widget
    self.layoutWidget = slicer.qMRMLLayoutWidget()
    self.layoutWidget.setMRMLScene(slicer.mrmlScene)
    self.frameParent.layout().addWidget(self.layoutWidget)
    self.layoutWidget.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUp3DView)
    
    self.threeDWidget = self.layoutWidget.layoutManager().threeDWidget(0)
    self.threeDWidget.threeDController().setVisible(False)

    self.threeDView = self.threeDWidget.threeDView()

    # Set up the Volumen rendering
    self.volRenLogic = slicer.modules.volumerendering.logic()
    self.setupCustomPreset()
    # Set the Default rendering method. They can be:
    #    - vtkMRMLCPURayCastVolumeRenderingDisplayNode (combobox: "VTK CPU Ray Casting" )
    #    - vtkMRMLGPURayCastVolumeRenderingDisplayNode (combobox: "VTK GPU Ray Casting" )
    #    - vtkMRMLMultiVolumeRenderingDisplayNode (combobox: "VTK Multi-Volume" )
    self.volRenLogic.SetDefaultRenderingMethod("vtkMRMLGPURayCastVolumeRenderingDisplayNode")

    # set up background color, box, label axis
    self.setup3DView()

    self.setupConnections()

    # Show defaul mummy (Mummy1)
    self.onLoadMummy1()

    #Full screen
    self.frameParent.showFullScreen() 
    self.frameParent.show()

  def setupConnections(self):
    logging.debug('Slicelet.setupConnections()')
    self.ui.mummyButton1.connect('clicked()', self.onLoadMummy1)
    self.ui.mummyButton2.connect('clicked()', self.onLoadMummy2)
    self.ui.viewButtonS.connect("clicked()", self.onViewSClicked)
    self.ui.viewButtonI.connect("clicked()", self.onViewIClicked)
    self.ui.viewButtonA.connect("clicked()", self.onViewAClicked)
    self.ui.viewButtonP.connect("clicked()", self.onViewPClicked)
    self.ui.viewButtonL.connect("clicked()", self.onViewLClicked)
    self.ui.viewButtonR.connect("clicked()", self.onViewRClicked)
    self.ui.volumeRenderingAButton.connect("clicked()", self.onOutsidePreset)
    self.ui.volumeRenderingBButton.connect("clicked()", self.onInsidePreset)

  # Disconnect all connections made to the slicelet to enable the garbage collector to destruct the slicelet object on quit
  def disconnect(self):
    self.ui.mummyButton1.disconnect('clicked()', self.onLoadMummy1)
    self.ui.mummyButton2.disconnect('clicked()', self.onLoadMummy2)
    self.ui.viewButtonS.disconnect("clicked()", self.onViewSClicked)
    self.ui.viewButtonI.disconnect("clicked()", self.onViewIClicked)
    self.ui.viewButtonA.disconnect("clicked()", self.onViewAClicked)
    self.ui.viewButtonP.disconnect("clicked()", self.onViewPClicked)
    self.ui.viewButtonL.disconnect("clicked()", self.onViewLClicked)
    self.ui.viewButtonR.disconnect("clicked()", self.onViewRClicked)
    self.ui.volumeRenderingAButton.connect("clicked()", self.onOutsidePreset)
    self.ui.volumeRenderingBButton.connect("clicked()", self.onInsidePreset)


  def setup3DView(self):
    bg_top = 0.05, 0.05, 0.05
    bg_btm = 0.36, 0.25, 0.2
   
    viewNode = self.threeDWidget.mrmlViewNode()
    viewNode.SetBoxVisible(False)
    viewNode.SetAxisLabelsVisible(False)
    viewNode.SetBackgroundColor(bg_top)
    viewNode.SetBackgroundColor2(bg_btm)

    self.threeDView.resetFocalPoint()
    self.threeDView.resetCamera()

  def onLoadMummy1(self):
    logging.debug('Slicelet.onLoadMummy1()')

    mummyName = 'Mummy1'
    dataFilename = 'Mummy1.nrrd'
    if mummyName == self.currentMummyName:  # Avoid unnecesary load of the current mummy
      return

    self.onLoadMummyX(dataFilename, mummyName)

  def onLoadMummy2(self):
    logging.debug('Slicelet.onLoadMummy2()')

    mummyName = 'Mummy2'
    dataFilename = 'Mummy2.nrrd'
    if mummyName == self.currentMummyName:  # Avoid unnecesary load of the current mummy
      return

    self.onLoadMummyX(dataFilename, mummyName)

  def onLoadMummyX(self, dataFilename, mummyName):
    logging.debug('Slicelet.onLoadMummyX()')

    # clean all generated node in mrml
    slicer.mrmlScene.Clear(0)
    self.setup3DView()
    self.currentMummyName = ''
    self.currentExplanation = ''

    moduleDir = os.path.dirname(__file__)
    volumenPath = os.path.join(moduleDir, 'Resources', 'Data', dataFilename)
    loadedVolumeNode = slicer.util.loadVolume(volumenPath)

    if loadedVolumeNode:
      volumeNode = slicer.util.getNode(mummyName)
      if volumeNode:
        self.currentMummyName = mummyName
        # Create all nodes and associated with VolumeNode
        displayNode = self.volRenLogic.CreateDefaultVolumeRenderingNodes(volumeNode)
        # Se tuo the outside preset
        self.onOutsidePreset()
        displayNode.SetVisibility(True)
        self.loadMummyExplanation(mummyName)
        self.showMummyExplanation(mummyName)
      else:
        logging.debug('Slicelet.onLoadMummyX(): No found the mummy node' + mummyName)
    else:
        logging.debug('Slicelet.onLoadMummyX(): No load the mummy' + mummyName)

    self.setup3DView()

  def loadMummyExplanation(self, mummyName):
    moduleDir = os.path.dirname(__file__)
    explanationPath = os.path.join(moduleDir, 'Resources', 'Data', mummyName + '.txt')

    explanationFile = open(explanationPath, "r")
    if (explanationFile.mode == 'r'):
      explanation = explanationFile.read()
      self.currentExplanation = explanation
    explanationFile.close()

  def showMummyExplanation(self, mummyName):
    self.ui.explanatoryText.setReadOnly(1)
    self.ui.explanatoryText.setPlainText(self.currentExplanation)

  def setupCustomPreset(self):
    moduleDir = os.path.dirname(__file__)
    presetsScenePath = os.path.join(moduleDir, 'Resources', 'VolRen', 'MyPresets.mrml')
    print(presetsScenePath)

    # Read presets scene
    customPresetsScene = slicer.vtkMRMLScene()
    vrPropNode = slicer.vtkMRMLVolumePropertyNode()
    customPresetsScene.RegisterNodeClass(vrPropNode)
    customPresetsScene.SetURL(presetsScenePath)
    customPresetsScene.Connect()

    # Add presets to volume rendering logic
    vrNodes = customPresetsScene.GetNodesByClass("vtkMRMLVolumePropertyNode")
    vrNodes.UnRegister(None)
    for itemNum in range(vrNodes.GetNumberOfItems()):
      node = vrNodes.GetItemAsObject(itemNum)
      self.volRenLogic.AddPreset(node)

  def onOutsidePreset(self):
    if self.currentMummyName:
      self.activatePreset('OutsidePreset')

  def onInsidePreset(self):
    if self.currentMummyName:
      self.activatePreset('InsidePreset')

  def activatePreset(self, PresetName):
    volumeNode = slicer.util.getNode(self.currentMummyName)
    if volumeNode:
      # Get the (Volumen Rendering) display node associated with the volume node
      displayNode = self.volRenLogic.GetFirstVolumeRenderingDisplayNode(volumeNode)
      # Copy the presert to a current displayNode
      displayNode.GetVolumePropertyNode().Copy(self.volRenLogic.GetPresetByName(PresetName))
    else:
      logging.debug('Slicelet.activatePreset(): No found the mummy node' + self.currentMummyName)

  def showPanel(self):
    self.uiWidget.show()

  def hidePanel(self):
    self.uiWidget.hide()


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
