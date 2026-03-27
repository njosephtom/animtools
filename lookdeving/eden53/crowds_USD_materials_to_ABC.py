
import maya.cmds as cmds


# Select your source and target meshes
#source_mesh = 'Crowd:DFS_Man_09__2004837513|Crowd:DFS_Man_09'
#target_mesh = 'Crowd1:DFS_Man_09_1891863527'

selected_objects = cmds.ls(selection=True)

source_mesh=selected_objects[0]
target_mesh=selected_objects[1]

# Copy UVs from the UVMap UV set to the default UV set
cmds.polyCopyUV(target_mesh, uvSetNameInput='UVMap', uvSetName='map1')


# Get the shape node of the mesh
source_shape_node = cmds.listRelatives(source_mesh, shapes=True)[0]
target_shape_node = cmds.listRelatives(target_mesh, shapes=True)[0]

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
            print(f"{target_mesh}.{faceIndexList}")
            #target_face = f"{target_mesh}.{"+faceIndexList+"}"
            target_face = f"{target_mesh}.{faceIndexList}"
            cmds.sets(target_face, edit=True, forceElement=sg)



