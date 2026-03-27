import os
import shutil
import maya.cmds as cmds
import maya.mel as mel
        
def collect_files(*args):
    # Get the output directory from the user
    folder_name = cmds.promptDialog(title="New Folder Name", message="Enter the name of the new folder:", button="OK", defaultButton="OK", cancelButton="Cancel")
    if folder_name == "OK":
        folder_name = cmds.promptDialog(query=True, text=True)
    if not folder_name:
        return
    output_dir = cmds.fileDialog2(fileMode=3, dialogStyle=2, )
    if not output_dir:
        return
    output_dir = output_dir[0]
    output_dir = os.path.join(output_dir, folder_name)
    
    # Create necessary subfolders
    sub_folders = ["scenes", "sourceimages"]
    if cmds.checkBox("subfoldersCB", query=True, value=True):
        sub_folders.extend(["assets", "autosave", "cache", "clips", "data", "images", "movies", "renderData", "sceneAssembly", "scripts", "Time Editor"])
    for folder in sub_folders:
        folder_path = os.path.join(output_dir, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            
   
    # Get a list of all external files used in the scene
    external_files = []
    audio_files = []
    for node_type in ["file", "AlembicNode", "audio"]:
        for node in cmds.ls(type=node_type):
            if node_type == "audio":
                file_path = cmds.getAttr(node + ".filename")
                if file_path and os.path.exists(file_path) and not file_path in audio_files:
                    audio_files.append(file_path)
            else:
                file_path = cmds.getAttr(node + ".fileTextureName") if node_type == "file" else cmds.getAttr(node + ".abc_File")
                if file_path and os.path.exists(file_path) and not file_path in external_files:
                    external_files.append(file_path)

    # Copy all external files to the output directory
    for file_path in external_files:
        file_name = os.path.basename(file_path)
        output_path = os.path.join(output_dir, "sourceimages", file_name)
        shutil.copy(file_path, output_path)
        
    # Copy all audio files to the sound subfolder
    if audio_files or (cmds.checkBox("subfoldersCB", query=True, value=True) and not audio_files):
        sound_folder = os.path.join(output_dir, "sound")
        if not os.path.exists(sound_folder):
            os.makedirs(sound_folder)
        for file_path in audio_files:
            file_name = os.path.basename(file_path)
            output_path = os.path.join(sound_folder, file_name)
            shutil.copy(file_path, output_path)

    # Get the current scene file path
    scene_file_path = cmds.file(query=True, sceneName=True)

    # Save the scene as a new file in the scenes folder
    if scene_file_path:
        scene_file_name = os.path.basename(scene_file_path)
        scene_file_ext = os.path.splitext(scene_file_name)[1]
        scene_file_name = os.path.splitext(scene_file_name)[0] + "_copy" + scene_file_ext
        scene_file_path = os.path.join(output_dir, "scenes", scene_file_name)
        cmds.file(rename=scene_file_path)
        cmds.file(save=True, options="v=0;", type="mayaAscii" if scene_file_path.endswith(".ma") else "mayaBinary")
    cmds.deleteUI("collectSceneWindow")

def create_collect_scene_ui():
    if cmds.window("collectSceneWindow", exists=True):
        cmds.deleteUI("collectSceneWindow")

    cmds.window("collectSceneWindow", title="Collect Scene Files")
    cmds.columnLayout()

    cmds.separator(height=10, style="in")

    cmds.checkBox("subfoldersCB", label="Add all project window subfolders?", value=False)
    cmds.text(label="If unchecked, only necessary subfolders will be created.")

    cmds.separator(height=10, style="in")
    cmds.text(label="Select output directory and save.")

    cmds.separator(height=10, style="in")

    cmds.button(label="Collect", command=collect_files)
    
    cmds.showWindow("collectSceneWindow")
    
create_collect_scene_ui()