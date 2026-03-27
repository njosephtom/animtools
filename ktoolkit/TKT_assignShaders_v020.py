import maya.cmds as cmds
import maya.mel as mel

# for texture copy and repath
import shutil
import os
import os.path


def sceneInfo():
    scenePath=cmds.file(q=True, sceneName=True) # name of scene file
    
    return scenePath


def referenceInfo():

    refPaths = []
    
    refAllFiles = cmds.ls(rf=True)
    print(refAllFiles)

    for reffile in refAllFiles:
    
        try: # error checking
            refPaths.append( cmds.referenceQuery( reffile ,filename=True ))
            print(refPaths)
        except:
            print("::: skipping UNKNOWN NODE REF ::: invalid ref node that connects to nothing or UNKNOWN nodes")
            pass

    return refPaths
    
# refPath = cmds.referenceQuery( rigGeoList[0], filename=True) # use rigGeoList mesh to find reference path
# P:/directors/cesar_pelizer/krog62_S03_P7_Ecomm/production/maya/lib/char/Kenzie/components/RIG/workshop/Kenzie_RIG_workshop_0006.ma
# P:/directors/cesar_pelizer/krog62_S03_P7_Ecomm/production/maya/lib/char/Kenzie/components/RIG/Kenzie_RIG.ma

def pathPrep(path):
    fileName = prepBaseName=os.path.split(path)[1]
    folderPath = prepBasePath=os.path.split(path)[0]
    
    return folderPath, fileName

def workshopPathConversion(path):

    splitWordPath = "workshop/"
    splitWordFile = "_workshop_"
    if path.find(splitWordPath) > -1:
        cleanBasePath = path.split(splitWordPath)[0]
        masterFilePath = cleanBasePath + path.split(splitWordPath)[1].split(splitWordFile)[0] + ".ma" # assume maya ascii
    else:
        masterFilePath = path

    if os.path.isfile(path) == True:
        return masterFilePath
    else:
        print(" !!! cannot find master file: " + masterFilePath)
        
    
def checkReferenceFiles(path):
    componentList = [ "RIG", "MDL", "SHD" ]
    
    for component in componentList:
        if path.find(component):
            return(component)
    
    
# TKT option

def listFiles(path):
    n = []
    files = os.listdir(path)
    
    folder = os.path.split(path)[0]
    
    if not os.path.exists(folder):
        #make folder
        print("NOT")
        os.makedirs(folder)


def TKTworkshopSAVE(folderPath, fileName):
    
    tktWorkshopPath = folderPath.replace("RIG", "TKT/workshop")
    tktWorkshopBaseName = fileName.replace("RIG", "TKT_workshop")

    if not os.path.exists(tktWorkshopPath):
        #make folder
        print("NOT")
        os.makedirs(tktWorkshopPath)

    tktWorkshopFiles = os.listdir(tktWorkshopPath)

    if not tktWorkshopFiles:
        print("empty folder")
        newTktWorkshopFileName = tktWorkshopPath +"/"+tktWorkshopBaseName.replace(".ma", "_0001.ma")
        print(newTktWorkshopFileName)
        
    else:
        n = []
        for tktFiles in tktWorkshopFiles:
            #print(tktFiles)
            
            if tktFiles.endswith("ma") and not tktFiles.startswith("."):
                n.append(os.path.splitext(tktFiles)[0].split("_")[-1])
                padding = len(n[0]) - 1
                #print(n)
                #print("length " + str(len(n)))
                
        
        # PADDING
        padding = len(n[0])
        nextTktFileNumber = int(max(n)) + 1
        print(str(nextTktFileNumber).rjust(padding, '0')) # insert Padding
        tktVersionNumber = str(nextTktFileNumber).rjust(padding, '0')
        
        # NEW TKT WORKSHOP FILE NAME
        
        newTktWorkshopFileName = tktWorkshopPath +"/"+tktWorkshopBaseName.replace(".ma", "_" + tktVersionNumber + ".ma")
        print(newTktWorkshopFileName)

    return newTktWorkshopFileName
    #saveFile(newTktWorkshopFileName)
    

#def makeProject():
    #make new maya project, under TKT
    #save maya file there
    #check if texture is not in folder and copy texture files to project
    #
    
def saveFile(path):
    # new FILE
    cmds.file( new=True, force=True)

    # save TKT file
    cmds.file( rename=path )
    cmds.file( save=True, type='mayaAscii' )


# ref in RIG
def referenceFile(path):
    print(" ref loading.....")
    
    if os.path.exists(path):
        cmds.file( path, reference=True, namespace="RIG")

        x = 0

        while x < 1:
            print(" ref loading.....")
            refNodes=cmds.ls( references=True )
            x = len(refNodes)

        print(" loaded and continue ")


def getTargetObjectList():

    
    # ----- List all objects below "*RIG:Geometry*"
    allRigGEO = cmds.ls( "*RIG:Geometry*", dag=True, ap=True )
    print(allRigGEO)

    if not allRigGEO or len(allRigGEO) == 1: # if can't find RIG:Geometry or found it but only a group / 1 item exists, then look further
        allRigGEO = cmds.ls( "*RIG:MDL*", dag=True, ap=True )

    return allRigGEO



def getTargetMeshList(allRigGEO):

    rigGeoList =[]

    for obj in allRigGEO:
        
        #print(cmds.objectType( obj ))
        shape = cmds.listRelatives(obj, shapes=True) or []# get the shape node
        
        try:
            meshPointCount = cmds.geometryAttrInfo(obj+".outMesh", pc=True) # if error then not an mesh
        except:
            print("not a mesh " + obj)
            meshPointCount = 0

        if len(shape) > 0 and meshPointCount > 0: # if a shape exists, then it's a mesh and added to the rigGeoList array
            rigGeoList.append(obj)
            print(obj)
    
    return rigGeoList    


def importShadeScene(path):
    if os.path.exists(path):
        # ----- import SHD scene
        #rigAssetPath = cmds.referenceQuery( rigGeoList[0], filename=True) # use rigGeoList mesh to find reference path
        #shdAssetPath = path.replace("RIG", "SHD") # replace RIG with SHD to get shade asset path

        cmds.file( path, i=True, namespace='SHD' ) # import shade asset with namespace SHD

        # ----- set ALL mesh in rig to lambert1
        allRigShapeObjs = cmds.ls(type='mesh', rn=True) # mesh and ref only
        cmds.sets(allRigShapeObjs, e=True, forceElement="initialShadingGroup")
    else:
        print("SHD PATH NOT FOUND")


def assignShaders(geoList):
    for obj in geoList:
        print(" ---------- ")
        print(obj)
        namespaceSplit = obj.split(":")
        print(namespaceSplit)
        
        #SHDobjectName = "SHD:" + obj.split(":")[-1] # geoList object (obj) and replace namespace to SHD
        SHDobjectName = obj.replace("RIG", "SHD")
        print(SHDobjectName)
        global RIGnamesapce
        RIGnamesapce = namespaceSplit[0] # save rig namespace for later
        namespaceLen = len(namespaceSplit)
        
        #my_extraNameSpacesList = namespaceSplit[1:-1]
        #print(my_extraNameSpacesList)
        
        
        if cmds.objExists(SHDobjectName): # check if object exist in SHD hierarchy
            #shdGeoList.append(SHDobjectName) # making a shd list
            print("SHD object exist = " + SHDobjectName)
            
            #if obj.find("|") > 0: # if there are duplicate name in GEO fine "|"
                #print("found duplicates")
                #cmds.select(obj.replace(RIGnamesapce, "SHD"), add=True) # replace multiple parts of name
                #SHDobjectName = obj.replace(RIGnamesapce, "SHD")
                #print(SHDobjectName)
               
            
            shape = cmds.listRelatives(SHDobjectName, shapes=True)# get the shape node
            print("shape " + str(shape))
            myShape = SHDobjectName +"|"+ shape[0]
            
            if obj.find("|") > 0: # if duplicates are found
                a = SHDobjectName.split("|")
                myShape = SHDobjectName +"|"+ shape[0]
                print(SHDobjectName +"|"+shape[0])
            
            shadingEngine = cmds.listConnections(myShape, type='shadingEngine') or [] # get the shading engine or empty array
            
            
            if len(shadingEngine) > 0: # if array is greater than 0 then apply shader to rig
                shading_group=shadingEngine[0]
                cmds.sets(obj, e=True, forceElement=shading_group) # assign the material to the object
                print("shd engine " + shadingEngine[0])
                print("assign shader")
        else:
           doesNotExistGeoList.append(obj) # keep a list to print later
           
           
        #return shdGeoList[0]

def cleanup(object):
    # ----- find the top of the SHD hierarchy so that I can delete the correct group

    cmds.select( object.replace("RIG","SHD") ) # select the first object in this array 
    checkParent = 1
    while checkParent > 0: # loop until the object has no parent
        aParent = cmds.pickWalk(d="up")
        parents = cmds.listRelatives(aParent, allParents=True)
        if parents:
            checkParent = 1
            
        else:
            checkParent = 0
            print(" This is the top most object in hierarchy ")
            print(checkParent)

    cmds.delete(aParent) # ----- delete the group
    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");') # ----- delete unused nodes
    
    
    # IMPORT LIGHTING AND RIG
    cmds.file(lightingSceneAsset, i=True ) # ----- import lighting asset
    cmds.file(rigMasterAssetPath, importReference=True) # ----- import references that are in scene ( should just be RIG now )
    
    
    
    # ----- namespaces
    cmds.namespace( rm='SHD', mergeNamespaceWithRoot=True ) # remove SHD namespace from remaining materials
    cmds.namespace( rm=RIGnamesapce, mergeNamespaceWithRoot=True ) # remove RIG namespace
    namespaces = cmds.namespaceInfo(listOnlyNamespaces=True)
    print(namespaces)


    # ----- namespaces EXTRA
    extraNamespaces = namespaces
    extraNamespaces.remove("UI")
    extraNamespaces.remove("shared")
    print(extraNamespaces)

    for nsList in extraNamespaces:
        print(nsList)
        #print(cmds.namespaceInfo(x, listOnlyDependencyNodes=True))
        y = cmds.namespaceInfo(nsList, listOnlyDependencyNodes=True)
        if not y:
            print(nsList + " = EMPTY namespace is REMOVED")
            cmds.namespace( rm=nsList, mergeNamespaceWithRoot=True ) 


def getTextures(path):

    print("")
    print("--- check texture section --- ")
    print("")


    localTexturePath=path.split("components")[0] + "textures/"
    print(localTexturePath)


    projectPath = path.split("production")[0]
    print("mainPath -> " + projectPath)

    # List all 2D textures that are also shaders
    cmds.listNodeTypes( 'file' )

    outsideTexturePathCollection = [] # set array variable

    # COLLECT all paths that are outside project path
    print("")
    print(" --- Collecting all paths outside project path --- ")

    allTextureFiles = cmds.ls(type="file")
    for tex in allTextureFiles:
        tFile = cmds.getAttr(tex + ".fileTextureName")
        print("")
        print(tex)
        #print("check: " + tex + " current pathed is: " + tFile)
        if tFile.find(localTexturePath) < 0 and len(tFile) > 0: # if project path is NOT found and not an empty file node
            print("result: NOT LOCAL -- > outside path: " + tex + " at " + str(tFile))
            outsideTexturePathCollection.append(tex)
            
        elif len(tFile) > 0: # otherwise project path found and file node not empty
            print("result: LOCAL ++ > local path " + tFile)
            #texturePath = tFile.split("textures")[0] + "textures/" # assign the texture folder path variable
            #texturePath=localTexturePath

    return outsideTexturePathCollection
    
def copyTextures(rigMasterFolderBase, outsideTexturePath):
    print("")
    print("--- copy texture section --- ")
    print("")

    for textureObject in outsideTexturePath:
        
        #check if file exists
        
        outsideTexturePath = cmds.getAttr(textureObject + ".fileTextureName")
        textureFileName = os.path.basename(outsideTexturePath)
        
        basePath = rigMasterFolderBase.split("components")[0]
        
        texturePath=basePath + "textures/"
        
        print(" Local Texture Folder is " + texturePath)
        
        if outsideTexturePath.find("hdr") > -1 or outsideTexturePath.find("HDR") > -1:
            texturePath = texturePath+"/hdr/"
            print(texturePath)
            if not os.path.isdir(texturePath):
                #make folder
                print(" Making HDR FOLDER in texture Folder")
                os.makedirs(texturePath)
        
            
        print("")
        #print("localPath is = " + texturePath)  
        #print(texturePath+textureFileName) # check if path combine looks right
        newPath = texturePath+textureFileName # combine correct texture path and file name
        print("+ new PATH should be = " + newPath)

        check_file_outside_exists = os.path.isfile(outsideTexturePath)
        
        print("original file exists : " + str(check_file_outside_exists))
        
        if check_file_outside_exists == True:
        
            check_file = os.path.isfile(newPath) # check if FILE EXIST on disk at destination folder result into variable
            print("+++ RESULT: " + str(check_file) + ", check if file already in folder" )
            if check_file == False: # if the file does not exist then copy file
                #print(newPath)
                
                print("--- file does not exiist --- ")
                print("--- copying " + outsideTexturePath)
                print("-------- to " + texturePath[:-1])
                shutil.copy2(outsideTexturePath, texturePath[:-1]) # COPY FILE, [:-1] removes the last character on the string... the last "/"
            else:
                print("+++ local texture file found " + newPath)
            cmds.setAttr(textureObject + ".fileTextureName", newPath, type="string") # set/update the scene FILE texture path
            print("++++ set Attr fileTextureName " )
            print(newPath)
            
        else:
            print("original file does not exist: " + outsideTexturePath)
                   

# ---------------------------------------------------------  START MAIN check paths -------------------------------------------------------

# ----- global array variables to hold selections
#lightingSceneAsset = "P:/directors/cesar_pelizer/krog00_library/production/assets/light_rigs/SHD_Char_LgtRig_ACES.ma"
lightingSceneAsset = "R:/assets/lookdev/kroger_lookdev_toolkit_template.ma"


refPathList = referenceInfo()

#get RIG component from ref ALWAYS
for refPath in refPathList:
    if checkReferenceFiles(refPath) == "RIG":
        rigMasterFile= workshopPathConversion(refPath)

rigMasterFolderBase, rigMasterFileBase = pathPrep(rigMasterFile)

print(rigMasterFolderBase)
print(rigMasterFileBase)

rigMasterAssetPath = rigMasterFolderBase +"/"+rigMasterFileBase

# where to save Tool Kit maya scene file?
newMayaFileName = TKTworkshopSAVE(rigMasterFolderBase, rigMasterFileBase)

# new FILE
cmds.file( new=True, force=True) # new file
saveFile(newMayaFileName ) # save init blank file

# ref in RIG
referenceFile(rigMasterAssetPath) # rig master file
rigGeoList = getTargetObjectList()
rigMeshList = getTargetMeshList(rigGeoList)

# apply shaders
importShadeScene( rigMasterAssetPath.replace("RIG","SHD") )
assignShaders(rigMeshList)

cleanup(rigGeoList[0])

# texture and files
texturePathList = getTextures(rigMasterFolderBase)
copyTextures(rigMasterFolderBase, texturePathList)

# save file
cmds.file( save=True, type='mayaAscii' )
print("File Saved")

# ---------------------------------------------------------  END MAIN check paths -------------------------------------------------------

# Set name to check and delete
set_name = "bakeSet"

# Check if it exists and is an objectSet
if cmds.objExists(set_name) and cmds.objectType(set_name) == "objectSet":
    cmds.delete(set_name)
    print("Deleted objectSet:", set_name)
else:
    print("ObjectSet '{}' does not exist or is not an objectSet.".format(set_name))
