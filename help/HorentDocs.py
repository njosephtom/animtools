import maya.cmds as cmds
import os
import random
password = "hornetdocs"
url = "https://app.milanote.com/1TB4xM1eB9aNfm/3d?p=QLrcz7uhFc5"
iconFolderPath = "P:/_lib/cg_lib/library/help/images/icons"

# by default, launch webpage and have password in clipboard
cmds.launch(web=url)
command = "echo {}| clip".format(password.strip())
os.system(command)

# open maya window incase artist wants to relaunch webpage or copy password
# Check if the window exists and delete it if it does
if cmds.window("exampleWindow", exists=True):
    cmds.deleteUI("exampleWindow", window=True)

# Create a new window with a fixed size
cmds.window("exampleWindow", title="3d Help", widthHeight=(220, 220), sizeable=False)

cmds.columnLayout( adjustableColumn=True )
cmds.separator( height=7, style='in' )
cmds.button( label='Open 3d docs', command='cmds.launch(web="{}")'.format(url) )
cmds.separator( height=7, style='in' )
cmds.button( label='Copy Password', command='os.system("echo {}| clip")'.format(password.strip()))

# Create a form layout
form = cmds.formLayout()

# Select an image from folder and display
imageFiles = [f for f in os.listdir(iconFolderPath) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
randomImage = random.choice(imageFiles)
randomImagePath = os.path.join(iconFolderPath, randomImage)
image = cmds.image(image=randomImagePath)

# Center the image in the form layout
cmds.formLayout(form, edit=True, attachForm=[(image, 'top', 20), (image, 'left', 40)])

cmds.showWindow("exampleWindow")