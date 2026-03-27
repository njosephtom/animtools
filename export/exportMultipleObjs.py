import maya.cmds as cmds
import os

# Get a list of selected objects
selected_objects = cmds.ls(selection=True)

if len(selected_objects) == 0:
    cmds.warning("Please select and object to export")

else:
    # Prompt the user for the location to export the files
    export_location = cmds.fileDialog2(fm=3, dir=os.path.expanduser('~'))[0]
    
    # Iterate over the selected objects
    for object in selected_objects:

        # Select object
        cmds.select(object)
        
        # Isolate the current object
        cmds.isolateSelect('modelPanel1', loadSelected=True)
           
        # Use the file command to export the object
        cmds.file( export_location + "/" + object + ".obj", type='OBJexport', exportSelected=True, force=True )
        
        # Reset the isolation
        cmds.isolateSelect('modelPanel1', state=False)