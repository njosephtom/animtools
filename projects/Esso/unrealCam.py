import maya.cmds as cmds

# save folder path
print( cmds.file( query=True, sceneName=True ))
sceneFullPath = cmds.file( query=True, sceneName=True )
folder_path = sceneFullPath.split("work")[0] + "/publish/camera/unreal"
print(folder_path)

# scene name
print( cmds.file( query=True, sceneName=True, shortName=True ) )
sceneName = cmds.file( query=True, sceneName=True, shortName=True )

cameraFileName = sceneName.replace("anim", "cameraMain").replace(".ma",".fbx")
print(cameraFileName)

version = cameraFileName.split(".")[0].split("_")[-1]
print(version)

full_folder_path = folder_path + "/" + version
print(full_folder_path)

userSelection = cmds.ls(sl=1)
print(userSelection)
shape_nodes = cmds.listRelatives(userSelection[0], shapes=True)


newCamera = cmds.camera(n="renderCamera")
new_shape_nodes = cmds.listRelatives(newCamera, shapes=True)


source_attributes = cmds.listAttr(new_shape_nodes[0], settable=True, multi=True, scalar=True)

# frame range
start_frame = cmds.playbackOptions(query=True, animationStartTime=True)
end_frame = cmds.playbackOptions(query=True, animationEndTime=True)


for att in source_attributes:
    print(att)
    attr_value = cmds.getAttr(shape_nodes[0]+"."+att)
    print(attr_value)
    
    cmds.setAttr(new_shape_nodes[0]+"."+att, attr_value)
    

cmds.parentConstraint( newCamera, userSelection[0], mo=False)

cmds.bakeResults(newCamera, simulation=True, t=(start_frame,end_frame), sampleBy=1, oversamplingRate=1, disableImplicitControl=True, preserveOutsideKeys=True, sparseAnimCurveBake=False, removeBakedAttributeFromLayer=False, removeBakedAnimFromLayer=False, bakeOnOverrideLayer=False, minimizeRotation=True, controlPoints=False, shape=True)

cmds.delete(cn=True) 

