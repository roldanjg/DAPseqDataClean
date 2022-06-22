from cdmanager import cd
import os
from pathlib import Path
import pandas as pd
import shutil
import subprocess
from utilpipeline import (
    extractBoxRegionAndMetType,
    mergeResultsMets
)


ids_file = '../data/commonData/ids_bisulfite_rep1_rep2.csv'
working_folder = '../data/bisulfite_rep1_rep2/'

idsDf = pd.read_csv(
            ids_file, 
            names=['id', 'rep', 'time', 'treatment']
                    )

with cd(working_folder):
    for index, id in idsDf.iterrows():

        targetFolder = os.path.join(id.rep, str(id.time), id.treatment)
        
        headname = '{}{}{}'.format(str(id.rep), str(id.time), id.treatment)

        extractBoxRegionAndMetType(targetFolder,headname)
        headname = '{}{}'.format( str(id.time), id.treatment)
        mergeResultsMets(targetFolder, headname)
        # intersectsFolder = os.path.join('intersections', id.tf)
        # Path(intersectsFolder).mkdir(parents=True, exist_ok=True)
        # sortBamFiles(targetFolder)
        # performIntersect(targetFolder, experimentTarget)
        # manageFolderLocationIntersects(intersectsFolder, targetFolder)
        # mergeResultsAmplifiedDirect(intersectsFolder, experimentTarget)



