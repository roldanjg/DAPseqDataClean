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

ids_file = '../data/commonData/ids_data_p.csv'
working_folder = '../data/data_p/'
raw_folder = '../raw_data_p'
working_folder_name = 'data_p'
bowtie2mode = '--sensitive'

with open(ids_file, 'r') as samplesOntology:
    idsDf = pd.read_csv(samplesOntology, names=['id', 'tf', 'type'])

with cd(working_folder):
    for index, id in idsDf.iterrows():
        gzs = []
        targetFolder = os.path.join(id.tf, str(id.type))
        inputControlpath = os.path.join(
                                '/home/joaquin/projects/methylation/data', working_folder_name, 'Input/{}'.format(id.type)
                            )
        performGEM(targetFolder, inputControlpath, working_folder_name)

