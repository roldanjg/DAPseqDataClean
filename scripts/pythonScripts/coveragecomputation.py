from cdmanager import cd
import os
from pathlib import Path
import pandas as pd
import shutil
import subprocess
from utilpipeline import (
    sortBamFiles,
    performIntersect,
    manageFolderLocationIntersects,
    mergeResultsAmplifiedDirect
)

def forERFs():
    return id.tf != 'MYC3' and id.tf != 'H7'

def forInput():
    return id.tf != 'MYC3' and id.tf != 'H7' and id.tf != 'ERF15' and id.tf != 'ERF1'

def forMYCs():
    return id.tf != 'ERF15' and id.tf != 'ERF1'

with open('../data/commonData/ids_data_rep1_coverage.csv', 'r') as samplesOntology:
    idsDf = pd.read_csv(samplesOntology, names=['id', 'tf', 'type', 'time', 'tratement'])

with cd('../data/tfs_rep_1/'):
    for index, id in idsDf.iterrows():
        if forInput():
            experimentTarget = 'Inputs'
        elif forERFs():
            experimentTarget = 'ERFs'
        elif forMYCs():
            experimentTarget = 'MYCs'

        targetFolder = os.path.join(id.tf, str(id.type), str(id.time), id.tratement)
        intersectsFolder = os.path.join('intersections', id.tf)
        Path(intersectsFolder).mkdir(parents=True, exist_ok=True)
        
        performIntersect(targetFolder, experimentTarget)
        manageFolderLocationIntersects(intersectsFolder, targetFolder)
        mergeResultsAmplifiedDirect(intersectsFolder, experimentTarget)



