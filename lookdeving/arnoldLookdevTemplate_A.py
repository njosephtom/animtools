import maya.cmds as cmds

# Specify the file path
file_path = "R:/assets/lookdev/lookdev_lgt_template.ma"



def open_scene_with_save_check(path):
    """Opens a Maya scene file, prompting the user to save if the current scene is unsaved."""

    # Check if the current scene is modified (unsaved)
    if cmds.file(query=True, modified=True):
        result = cmds.confirmDialog(
            title="Unsaved Changes",
            message="The current scene has unsaved changes. Do you want to save?",
            button=["Save", "Don't Save", "Cancel"],
            defaultButton="Save",
            cancelButton="Cancel",
            dismissString="Cancel"
        )

        if result == "Save":
            if cmds.file(query=True, ex=True):
                print("file exists")
                cmds.file(save=True)
            else:
                save_with_browse()
        elif result == "Cancel":
            return  # Don't open a new scene
            
            
    # Open the file
    cmds.file(path, open=True, force=True)

def save_with_browse():
    """Saves the current Maya scene with a browse dialog."""

    file_path = cmds.fileDialog2(fileMode=0, caption="Save Scene As")

    if file_path:
        cmds.file(rename=file_path[0])
        cmds.file(save=True, type="mayaAscii") 


open_scene_with_save_check(file_path)