# windows > general editors > file path editor
# select texture or textures and run script
# if script see N drive, it will replace with /mnt/eden2

import maya.cmds as cmds

userSelection = cmds.ls(sl=1)
print(userSelection)

def setLocal(userSelection):
    for eachFile in userSelection:
        path2 = cmds.getAttr(eachFile +".fileTextureName")
        print(path2)
        if "mnt/eden2" in path2:
            
            cmds.setAttr(eachFile +".fileTextureName", path2.replace("/mnt/eden2","N:" ), type="string" )
            
            path2 = cmds.getAttr(eachFile +".fileTextureName")
            print(path2)

def setAWS(userSelection):
    for eachFile in userSelection:
        path2 = cmds.getAttr(eachFile +".fileTextureName")
        print(path2)
        if "N:" in path2:
            
            cmds.setAttr(eachFile +".fileTextureName", path2.replace("N:","/mnt/eden2"), type="string" )
            
            path2 = cmds.getAttr(eachFile +".fileTextureName")
            print(path2)
        
        
#setLocal(userSelection)       
setAWS(userSelection)