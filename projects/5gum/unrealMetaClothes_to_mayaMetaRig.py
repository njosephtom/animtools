
# this script will use the last selection to determine if it needs to account for a reference rig to contrain to.

# usage: select the hierarchy of the imported metahuman clothing fbx
# example: select root then go to Select > Hierarchy, then CTRL + select a single reference rig object
# reference rig object: can be any object, like a group or a joint, the script is just trying to extract the namespace

userSelection = cmds.ls(sl=1)
print(userSelection)


if len(userSelection) == 0:
    # open maya window incase artist wants to relaunch webpage or copy password
    # Check if the window exists and delete it if it does
    if cmds.window("hhelp", exists=True):
        cmds.deleteUI("hhelp", window=True)

    # Create a new window with a fixed size
    cmds.window("hhelp", title="Help", sizeable=False)

    cmds.columnLayout( adjustableColumn=True )
    cmds.text( label="")
    cmds.text( label='this script will use the last selection to determine if it needs to account for a reference rig to contrain to.' )
    cmds.text( label="usage: select the hierarchy of the imported metahuman clothing fbx")
    cmds.text( label="example: select root then go to Select > Hierarchy, then CTRL + select a single reference rig object")
    cmds.text( label="reference rig object: can be any object, like a group or a joint, the script is just trying to extract the namespace")
    cmds.text( label="")
    cmds.separator( height=7, style='in' )
    cmds.text( label="")
    cmds.showWindow("hhelp")



refnamesapce = ""

# remove the last selection and assing it to a variable to check for ref namespaces
rigselection = userSelection.pop()
print(rigselection)

# check if the last item in selection is a reference with name space, if true, then assign namespace to refnamesapce variable
if rigselection.find(":") > 0:
    print("it's a rig")
    refnamesapce = rigselection.split(":")[0] + ":"
    print("rig name space is " + refnamesapce)
    refnamesapce
    
# loop through the clothing rig selection and contrain to each joint on rig
for elem in userSelection:

    cmds.parentConstraint( refnamesapce + elem + '_drv', elem )