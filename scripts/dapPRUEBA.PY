from cdmanager import cd
import os
from pathlib import Path
import pandas as pd
import shutil
import subprocess
from utilpipeline import (
    checkMD5isCorrect,
    checkFastaQLenght,
    performTrimGalore,
    qualityCheckTrimGalore,
    performBowtie2,
    getBamAndDeleteSam,
    sortBamFiles,
    performGEM
)

ids_file = '../data/commonData/ids_data_rep_3.csv'
working_folder = '../data/tfs_rep_3_input_from_rep_2/'
raw_folder = '../raw_data_rep_3'
working_folder_name = 'tfs_rep_3_input_from_rep_2'
bowtie2mode = '--sensitive'

with open(ids_file, 'r') as samplesOntology:
    idsDf = pd.read_csv(samplesOntology, names=['id', 'tf', 'type', 'time', 'tratement'])

with cd(working_folder):
    for index, id in idsDf.iterrows():
        gzs = []
        targetFolder = os.path.join(id.tf, str(id.type), str(id.time), id.tratement)

        inputControlpath = os.path.join(
            '/home/bgp01/methylation/data', working_folder_name, 'Input/amplified',
            f'{id.time}/{id.tratement}'
        )
        print(inputControlpath)
        performGEM(targetFolder, inputControlpath, working_folder_name)

