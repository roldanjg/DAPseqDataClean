from cdmanager import cd
import os
from pathlib import Path
import pandas as pd
import shutil
from utilpipeline import (
    performBigWigextraction
)

ids_file = '../data/commonData/ids_replica_2.csv'
bigWigFolder = '../../../../../bigwigs/replicate2/'
# -------
headPaths = {
    'Pool_': '/home/joaquin/projects/methylation/data/tfs_rep_1',
    'JM10-': '/home/joaquin/projects/methylation/data/tfs_rep_3_input_from_rep_2',
    'JM9-': '/home/joaquin/projects/methylation/data/tfs_rep_3_input_from_rep_2',
    'JM6INDEX': '/home/joaquin/projects/methylation/data/tfs_rep_2'
}

with open(ids_file, 'r') as samplesOntology:
    idsDf = pd.read_csv(samplesOntology, names=['id', 'path'])


for index, id in idsDf.iterrows():
    for idHeads in headPaths:
        if idHeads in id.id:
            targetFolder = os.path.join(headPaths[idHeads] ,id.path)
    print(targetFolder)
    file_names = os.listdir(targetFolder)
    itsdone = False
    for file in file_names:
        if 'coverage.bw' in file:
            print('hola')
            itsdone = True
    
    if not itsdone:
        print('nohola')
        performBigWigextraction(targetFolder)

    with cd(targetFolder):
        file_names = os.listdir()
        for file in file_names:
            if 'coverage.bw' in file:
                bigw = file
                originalfolder = os.path.join(
                    bigw
                )
                finalFolder = os.path.join(
                    bigWigFolder
                )
                print(originalfolder, finalFolder)
                shutil.copy2(bigw, finalFolder)