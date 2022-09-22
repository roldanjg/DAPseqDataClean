from cdmanager import cd
import os
import shutil
from pathlib import Path

working_folder = '/home/joaquin/projects/methylation/data/data_Fragaria_vesca_Pose'
destination_folder = '/home/joaquin/projects/methylation/data/gemFiles/gem_Fragaria_vesca_Pose'

with cd(working_folder):
    for root, dirs, files in os.walk('./'):
        #print(dirs)
        if 'GEMout' in dirs:
            namedir = str(root.replace('./', ''))
            originalfolder = os.path.join(
                namedir,
                'GEMout'
            )
            finalFolder = os.path.join(
                destination_folder,
                str(root).replace('/', '').replace('.', '')+'GEMout'
            )
            print(originalfolder, finalFolder)
            shutil.copytree(originalfolder, finalFolder)

