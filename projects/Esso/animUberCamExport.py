import maya.cmds as cmds
import os
import shutil

def export_fbx_with_baked_animation(file_path, start_frame, end_frame, step_value=1):
    """
    Exports the selected objects to an FBX file with baked animation.

    Args:
        file_path (str): The full path to save the FBX file.
        start_frame (int): The start frame for baking the animation.
        end_frame (int): The end frame for baking the animation.
        step_value (int, optional): The step value for baking (e.g., 1 for every frame). Defaults to 1.
    """
    #if not cmds.pluginInfo('fbxmaya', query=True, loaded=True):
    #    cmds.loadPlugin('fbxmaya')

    
    # Set FBX export options for baking animation
    mel.eval('FBXResetExport;') # Reset FBX export settings
    mel.eval('FBXExportSkins -v true;') # Export skinned meshes
    #cmds.mel.eval('FBXExportShapes -v true;') # Export blend shapes
    #cmds.mel.eval('FBXExportCameras -v true;') # Export cameras
    mel.eval('FBXExportLights -v true;') # Export lights
    mel.eval('FBXExportAnimationOnly -v false;') # Export geometry and animation
    #mel.eval('FBXExportBakeAnimation -v true;') # Enable baking animation
    mel.eval('FBXExportBakeComplexAnimation -v true')
    mel.eval('FBXExportBakeComplexStart -v {}'.format(start_frame))
    mel.eval('FBXExportBakeComplexEnd -v {}'.format(end_frame))
    mel.eval('FBXExportBakeComplexStep -v 1') # Bake every frame
    #mel.eval(f'FBXExportBakeFrameStart -v {start_frame};')
    #mel.eval(f'FBXExportBakeFrameEnd -v {end_frame};')
    #mel.eval(f'FBXExportBakeFrameStep -v {step_value};')
    #mel.eval('FBXExportResampleAll -v true;') # Resample all animation

    # Export selected objects to FBX
    cmds.file(file_path, force=True, options='v=0;', type='FBX export', exportSelected=True)
    print(f"Successfully exported FBX with baked animation to: {file_path}")




def make_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")


# save folder path

print( cmds.file( query=True, sceneName=True ))
sceneFullPath = cmds.file( query=True, sceneName=True )
folder_path = sceneFullPath.split("work")[0] + "/publish/unreal"
print(folder_path)
version_folder_path = folder_path + "/versions"

make_folder(folder_path)
make_folder(version_folder_path)

# scene name
print( cmds.file( query=True, sceneName=True, shortName=True ) )
sceneName = cmds.file( query=True, sceneName=True, shortName=True )

cameraFileName = sceneName.replace("anim", "cameraMain").replace(".ma",".fbx")
print(cameraFileName)

version = cameraFileName.split(".")[0].split("_")[-1]
print(version)

versionFilePath = folder_path + "/" + cameraFileName[7:]
print(versionFilePath)
masterFilePath = versionFilePath.replace("_"+version,"")
print(masterFilePath)


userSelection = cmds.ls(sl=1)
print(userSelection)
shape_nodes = cmds.listRelatives(userSelection[0], shapes=True)


newCamera = cmds.camera(n="renderCamera")
new_shape_nodes = cmds.listRelatives(newCamera, shapes=True)

newCamera = cmds.ls(sl=1)

source_attributes = cmds.listAttr(new_shape_nodes[0], settable=True, multi=True, scalar=True)

# frame range -- set the scene frame range for unreal to read in +1 at end
start_frame = cmds.playbackOptions(query=True, animationStartTime=True)
end_frame = cmds.playbackOptions(query=True, animationEndTime=True) + 1
cmds.playbackOptions(animationEndTime=end_frame)
cmds.playbackOptions(maxTime=end_frame)

for att in source_attributes:
    print(att)
    attr_value = cmds.getAttr(shape_nodes[0]+"."+att)
    print(attr_value)
    
    cmds.setAttr(new_shape_nodes[0]+"."+att, attr_value)
    

cmds.parentConstraint( userSelection[0], newCamera[0], mo=False)

cmds.bakeResults(newCamera[0], simulation=True, t=(start_frame,end_frame), sampleBy=1, oversamplingRate=1, disableImplicitControl=True, preserveOutsideKeys=True, sparseAnimCurveBake=False, removeBakedAttributeFromLayer=False, removeBakedAnimFromLayer=False, bakeOnOverrideLayer=False, minimizeRotation=True, controlPoints=False, shape=True)

cmds.select(newCamera[0])
cmds.delete(cn=True) 

export_fbx_with_baked_animation(versionFilePath, start_frame, end_frame)

try:
    # Copy the file to the destination with the new name
    shutil.copy(versionFilePath, masterFilePath)
    print(f"File '{versionFilePath}' copied to '{masterFilePath}' and renamed.")
except FileNotFoundError:
    print(f"Error: Source file '{versionFilePath}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")
    
    
cmds.playbackOptions(animationEndTime=end_frame - 1)
cmds.playbackOptions(maxTime=end_frame - 1)


# MOVE version files into versions folder
try:
    # Ensure the destination directory exists (optional, shutil.move can create it)
    if not os.path.exists(version_folder_path):
        os.makedirs(version_folder_path)

    # Move the file
    shutil.move(versionFilePath, version_folder_path)
    print(f"File '{versionFilePath}' moved successfully to '{version_folder_path}'")

except FileNotFoundError:
    print(f"Error: Source file '{versionFilePath}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")
    
