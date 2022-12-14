from cdmanager import cd
import os
from pathlib import Path
import pandas as pd
import shutil
import subprocess
from utilpipeline import (
    performBedGraphextraction
)

ids_file = '/home/joaquin/projects/methylation/data/commonData/ids_data_dobles_JM15.csv'
working_folder_name = '/home/joaquin/projects/methylation/data/data_dobles_JM15'
bigWigFolder = '/home/joaquin/projects/methylation/data/bigwigs/arebadornot_jm15'

with open(ids_file, 'r') as samplesOntology:
    idsDf = pd.read_csv(samplesOntology, names=['id', 'replicate', 'condition', 'experimentid',  'inputid'])

with cd(working_folder_name):
    for index, id in idsDf.iterrows():
        targetFolder = os.path.join(id.replicate,id.condition,str(id.experimentid),str(id.inputid))
        performBedGraphextraction(targetFolder)
        with cd(targetFolder):
            file_names = os.listdir()
            for file in file_names:
                if 'coverage.bedgraph' in file:
                    bigw = file
                    originalfolder = os.path.join(
                        bigw
                    )
                    finalFolder = os.path.join(
                        bigWigFolder
                    )
                    print(originalfolder, finalFolder)
                    shutil.copy2(bigw, finalFolder)