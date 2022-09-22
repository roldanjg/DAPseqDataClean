from cdmanager import cd
import os
from pathlib import Path
import pandas as pd
import shutil
import subprocess
from utilpipeline import (
    sortBamFiles,
    performBigWigextraction
)

ids_file = '../data/commonData/ids_data_amino_mutant.csv'
working_folder_name = '../data/data_amino_muts/'
bigWigFolder = '../../../../../bigwigs/loop/'

with open(ids_file, 'r') as samplesOntology:
    idsDf = pd.read_csv(samplesOntology, names=['id', 'tf', 'type'])

with cd(working_folder_name):
    for index, id in idsDf.iterrows():
        targetFolder = os.path.join(id.tf, str(id.type))
        sortBamFiles(targetFolder)
        performBigWigextraction(targetFolder)
        #with cd(targetFolder):
        #    file_names = os.listdir()
        #    for file in file_names:
        #        if 'coverage.bw' in file:
        #            bigw = file
        #            originalfolder = os.path.join(
        #                bigw
        #            )
        #            finalFolder = os.path.join(
        #                bigWigFolder
        #            )
        #            print(originalfolder, finalFolder)
        #            shutil.copy2(bigw, finalFolder)
        #