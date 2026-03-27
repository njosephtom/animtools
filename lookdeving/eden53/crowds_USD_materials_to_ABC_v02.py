
import maya.cmds as cmds


# Select your source and target meshes
#source_mesh = 'Crowd:DFS_Man_09__2004837513|Crowd:DFS_Man_09'
#target_mesh = 'Crowd1:DFS_Man_09_1891863527'

selected_objects = cmds.ls(selection=True)

source_mesh=selected_objects[0]
#target_mesh=selected_objects[1]

print(source_mesh)

print(source_mesh.split(":")[1])
splitSelectionNameList = source_mesh.split(":")[1]
if "Man_" in splitSelectionNameList:
    print("found man")
    
    print(splitSelectionNameList.split("_"))
    splitAgain = splitSelectionNameList.split("_")
    splitAgain.pop()
    print(splitAgain)
    print("_".join(splitAgain))
    searchName = "_".join(splitAgain)

    if len(splitAgain) == 3:
        splitAgain.append("")
    print("len of array 3 of source = " + str(len(splitAgain[3])) )    
    
    if len(splitAgain[3]) == 2:
        manVersion = 1
    else:
        manVersion = 0

    

actorName = "Crowd:"+searchName+"*"
print("****")

#actorName = "Crowd:"+source_mesh.split(":")[-1]+"*"

cmds.select(actorName)
selected_objects_abc = cmds.ls(selection=True)

finalList = []

for item in selected_objects_abc:
    print(item)

    a = item.split("_")
    print("len of array3 = " + str( len(a[3]) ) )
    if len(a[3]) == 2:
        print(item + " > removing this from list ")
        if manVersion == 1:
            finalList.append(item)
    else:
        finalList.append(item)

print(finalList)
cmds.select(finalList)




# Get the shape node of the mesh
source_shape_node = cmds.listRelatives(source_mesh, shapes=True)[0]
#target_shape_node = cmds.listRelatives(target_mesh, shapes=True)[0]

print(source_mesh + "|" + source_shape_node)
source_shape_node_1 = source_mesh + "|" + source_shape_node



# Get the shading groups and their corresponding faces from the source mesh
shading_groups = cmds.listConnections(source_shape_node_1, type='shadingEngine')
for sg in shading_groups:
    # Get the faces assigned to the shading group
    faces = cmds.sets(sg, query=True)
    if faces:
        
        indexList = []
        
        # Assign the shading group to the corresponding faces on the target mesh
        for face in faces:
            face_index = face.split('.')[-1]
            indexList.append(face_index)
            #target_face = f"{target_mesh}.{face_index}"
            #cmds.sets(target_face, edit=True, forceElement=sg)
        
        my_list = list(set(indexList))
        print()
        print(sg)
        print(my_list)
        
        
        
        for faceIndexList in my_list:
            
            for target_mesh in finalList:
                
                # Copy UVs from the UVMap UV set to the default UV set
                cmds.polyCopyUV(target_mesh, uvSetNameInput='UVMap', uvSetName='map1')

            
                print(f"{target_mesh}.{faceIndexList}")
                #target_face = f"{target_mesh}.{"+faceIndexList+"}"
                target_face = f"{target_mesh}.{faceIndexList}"
                cmds.sets(target_face, edit=True, forceElement=sg)



