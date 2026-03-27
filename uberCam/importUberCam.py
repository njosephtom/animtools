import maya.cmds as cmds

# Importing the Maya binary file with specified options
cmds.file('P:/_lib/cg_lib/ubercam/Ubercamera_rig.mb', 
          i=True, 
          type='mayaBinary', 
          ignoreVersion=True, 
          mergeNamespacesOnClash=False, 
          rpr='Ubercamera_rig', 
          options='v=0;', 
          pr=True, 
          importFrameRate=True, 
          importTimeRange='override')

# Loading required node types
cmds.requires('Type', '2.0a', nodeType='type')
cmds.requires('shellDeformer', nodeType='shellDeformer')
cmds.requires('vectorAdjust', nodeType='vectorAdjust')
cmds.requires('typeExtrude', nodeType='typeExtrude')

# Loading required plugins
cmds.requires('mtoa', '5.3.4.1', nodeType='aiOptions')
cmds.requires('mtoa', '5.3.4.1', nodeType='aiAOVDriver')
cmds.requires('mtoa', '5.3.4.1', nodeType='aiAOVFilter')

# Loading stereoCamera plugin
cmds.requires('stereoCamera', '10.0')