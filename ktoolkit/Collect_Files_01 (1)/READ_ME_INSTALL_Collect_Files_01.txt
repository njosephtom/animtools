Install Collect_Files_01.py


1. Put the file, "Collect_Files_01.py" in your scripts folder for the Maya version you are using. Example: C:\Users\user\Documents\maya\2023\scripts
2. Open the script editor and run the python script, that matches the maya version you are using, to import and run the script.


Maya 2022/2023

import maya.cmds as cmds
import os
script_path = os.path.join(cmds.internalVar(userScriptDir=True), 'Collect_Files_01.py')
with open(script_path, 'r') as f:
        script_contents = f.read()
exec(script_contents)



Maya 2020

import maya.cmds as cmds
import os
script_path = os.path.join(cmds.internalVar(userScriptDir=True), 'Collect_Files_01.py')
execfile(script_path)



3. Save the above script to your shelf for easy access.




*****
The only thing it doesn't do (yet) is collect any referenced files - that will be version 2 :) Temporary solve is to important any references into the scene before running the script.


I've tested this in Maya 2020 and it works, but let me know if you run into any issues.
