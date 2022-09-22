from cdmanager import cd
import os
from pathlib import Path
import pandas as pd
import shutil
import subprocess
from utilpipeline import (
    performIntersect,
    manageFolderLocationIntersects,
    mergeResultsAmplifiedDirect
)

def forERFs():
    return  'ERF15' in id.path or  'ERF1' in id.path

def forInput():
    return  'Input' in id.path

def forMYCs():
    return  'MYC3' in id.path or  'MYCH7' in id.path  

 
#  need to modify this in each experiment
idsDf = pd.read_csv(
            '../data/commonData/ids_replica_3.csv', 
            names=['id', 'path']
                    )
intersectionsPath = '/home/joaquin/projects/methylation/data/intersects/rep3'
# -------
headPaths = {
    'Pool_': '/home/joaquin/projects/methylation/data/tfs_rep_1',
    'JM10-': '/home/joaquin/projects/methylation/data/tfs_rep_3_input_from_rep_2',
    'JM9-': '/home/joaquin/projects/methylation/data/tfs_rep_3_input_from_rep_2',
    'JM6INDEX': '/home/joaquin/projects/methylation/data/tfs_rep_2',
    'JM-30': '/home/joaquin/projects/methylation/data/tfs_rep_4',
}


for index, id in idsDf.iterrows():
    if forInput():
        experimentTarget = 'Inputs'
    elif forERFs():
        experimentTarget = 'ERFs'
    elif forMYCs():
        experimentTarget = 'MYCs'
    for idHeads in headPaths:
        if idHeads in id.id:
            targetFolder = os.path.join(headPaths[idHeads] ,id.path)
            # print(targetFolder)

    
    intersectsFolder = os.path.join(intersectionsPath, id.path.split('/')[0])
    # print(intersectsFolder)
    Path(intersectsFolder).mkdir(parents=True, exist_ok=True)
    performIntersect(targetFolder, experimentTarget)
    manageFolderLocationIntersects(intersectsFolder, targetFolder)
    mergeResultsAmplifiedDirect(intersectsFolder, experimentTarget)



