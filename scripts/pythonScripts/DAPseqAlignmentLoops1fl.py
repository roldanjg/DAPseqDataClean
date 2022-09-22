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

ids_file = '../data/commonData/ids_data_loops_fl_1.csv'
working_folder = '../data/data_loops_fl_1/'
raw_folder = '../raw_data_rep_4'
working_folder_name = 'data_loops_fl_1'
bowtie2mode = '--sensitive'

with open(ids_file, 'r') as samplesOntology:
    idsDf = pd.read_csv(samplesOntology, names=['id', 'tf', 'type'])

with cd(working_folder):
    for index, id in idsDf.iterrows():
        gzs = []
        targetFolder = os.path.join(id.tf, str(id.type))
        Path(targetFolder).mkdir(parents=True, exist_ok=True)

        originalfolder = os.path.join(raw_folder, id.id)
        file_names = os.listdir(originalfolder)
        if len(file_names) >= 2:
            #  gz + MD5 in case of single-read or 2 gzs and MD5 in case of pair-ends, more if divided long files
            print('Checking MD5 from ' + id.id)
            if checkMD5isCorrect(originalfolder):
                print('Checking Fastaq lenghts from ' + id.id)
                if checkFastaQLenght(originalfolder):
                    for fileInside in file_names:
                        if 'gz' in fileInside:
                            gzs.append((fileInside))
                            originalFile = os.path.join(originalfolder, fileInside)
                            shutil.move(originalFile, targetFolder)

                    print('Doing Trim galore in ' + targetFolder + ' from ' + id.id)
                    performTrimGalore(targetFolder)
                    for file in gzs:
                        destinationFile = os.path.join(targetFolder, file)
                        shutil.move(destinationFile, originalfolder)
                    print('Trim galore finished,checking results...')
                    if qualityCheckTrimGalore(targetFolder):
                        samfileexperiment = '{}{}.sam'.format(id.tf, str(id.type))
                        print('Doing Bowtie2 in ' + targetFolder + ' from ' + id.id)
                        performBowtie2(
                            targetFolder,
                            bowtie2mode,
                            samfileexperiment
                                       )
                        getBamAndDeleteSam(targetFolder)
                        sortBamFiles(targetFolder)
                        if id.tf == 'Input':
                            print('this is an input file so dont do GEM!')
                        else:
                            inputControlpath = os.path.join(
                                '/home/joaquin/projects/methylation/data', working_folder_name, 'Input/Input'
                            )
                            performGEM(targetFolder, inputControlpath, working_folder_name)

