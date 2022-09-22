from cdmanager import cd
import os
from pathlib import Path
import pandas as pd
import shutil
import subprocess
from utilpipeline import (
    performBigWigextraction
)

ids_file = '/home/joaquin/projects/methylation/data/commonData/ids_data_MYC2_Full_Lenght_WT.csv'
working_folder_name = '/home/joaquin/projects/methylation/data/data_MYC2_Full_Lenght_WT'
bigWigFolder = '/home/joaquin/projects/methylation/data/bigwigs/bw_MYC2_Full_Lenght_WT'

with open(ids_file, 'r') as samplesOntology:
    idsDf = pd.read_csv(samplesOntology, names=['id', 'tf', 'rep'])

with cd(working_folder_name):
    for index, id in idsDf.iterrows():
        targetFolder = os.path.join(id.tf,id.rep)
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