import maya.cmds as cmds
import os

# save folder path

print( cmds.file( query=True, sceneName=True ))
sceneFullPath = cmds.file( query=True, sceneName=True )
folder_path = sceneFullPath.split("work")[0] + "/publish/cars"
print(folder_path)

if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"Folder '{folder_path}' created successfully.")
else:
    print(f"Folder '{folder_path}' already exists.")




# scene name
print( cmds.file( query=True, sceneName=True, shortName=True ) )
sceneName = cmds.file( query=True, sceneName=True, shortName=True )

shortSceneName = sceneName[7:].replace(".ma","")
print(shortSceneName)

# selection
userSelection = cmds.ls(sl=1)
print(userSelection)

# loop
for elem in userSelection:
    
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
        
        	
        cmds.file(saveFilePath, force=True, options="v=0;", typ="FBX export", pr=True, es=True)
        
        
#file -force -options "v=0;" -typ "FBX export" -pr -es "P:/projects/essoMobil/esso03_bobbles/scratch/pakorn/fbxTestExports/esso03_bobble/eb3_0010/publish/cars/testtesttest.fbx";
