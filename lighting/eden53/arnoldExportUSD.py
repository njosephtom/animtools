# arnold export selection as USD
# select a object and run script


import maya.mel as mel

path = "N:/eden53_production/assets/env/MG_City/work/mdl/hardcodePath_usd_export"

userSelection = cmds.ls(sl=1)
print(userSelection)

for elem in userSelection:
    path_file = path + "/" + elem +"_aws.usd"

    mel_command = 'arnoldExportAss -f \"{}\" -s -boundingBox -mask 6399 -lightLinks 1 -shadowLinks 1;'.format(path_file)
    
    #print(mel_command)
    
    # Execute the MEL command
    mel.eval(mel_command)