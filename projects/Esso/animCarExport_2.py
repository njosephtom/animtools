import maya.cmds as cmds
import os
import maya.mel as mel
import shutil


# save over same file but make a note of versions exported



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

# Example usage:
# Select the objects you want to export in Maya before running this.
# Replace with your desired file path and frame range.
# export_fbx_with_baked_animation("C:/temp/my_baked_animation.fbx", 1, 100)



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

# frame range
start_frame = cmds.playbackOptions(query=True, animationStartTime=True)
end_frame = cmds.playbackOptions(query=True, animationEndTime=True) + 1
cmds.playbackOptions(animationEndTime=end_frame)
cmds.playbackOptions(maxTime=end_frame)

# scene name
print( cmds.file( query=True, sceneName=True, shortName=True ) )
sceneName = cmds.file( query=True, sceneName=True, shortName=True )

shortSceneName = sceneName[7:].replace(".ma","")
print(shortSceneName)

# selection
userSelection = cmds.ls(sl=1)
print(userSelection)


# unique namespace list 
nn = []
for obj in userSelection:
    nn.append(obj.split(":")[0])
    
print(nn)

# Remove duplicates using a set
unique_namespaces = list(set(nn))
print(unique_namespaces)



# loop
for elem in unique_namespaces:
    
    cmds.select(cl=True)
    
    elemNameSpace = elem.split(":")[0]
    print(elemNameSpace)
    
    carFileName = shortSceneName.replace("anim", elemNameSpace)
    print(carFileName)
    
    saveFilePath = folder_path + "/" + carFileName + ".fbx"
    print(saveFilePath) 
    
    exportSelectionList = ["DeformationSystem", "Geometry"]
    for sel in exportSelectionList:
        cmds.select(elemNameSpace+":"+sel, add=True, hi=True)
             	
        #cmds.file(saveFilePath, force=True, options="v=0;", typ="FBX export", pr=True, es=True)
                
        export_fbx_with_baked_animation(saveFilePath, start_frame, end_frame)

        #file -force -options "v=0;" -typ "FBX export" -pr -es "P:/projects/essoMobil/esso03_bobbles/scratch/pakorn/fbxTestExports/esso03_bobble/eb3_0010/publish/cars/testtesttest.fbx";

        masterFilename = saveFilePath.split("_v")[0] + ".fbx"

        try:
            # Copy the file to the destination with the new name
            shutil.copy(saveFilePath, masterFilename)
            print(f"File '{saveFilePath}' copied to '{masterFilename}' and renamed.")
        except FileNotFoundError:
            print(f"Error: Source file '{saveFilePath}' not found.")
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
    shutil.move(saveFilePath, version_folder_path)
    print(f"File '{saveFilePath}' moved successfully to '{version_folder_path}'")

except FileNotFoundError:
    print(f"Error: Source file '{saveFilePath}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")