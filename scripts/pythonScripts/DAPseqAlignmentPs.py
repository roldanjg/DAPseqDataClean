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
    performGEM,
    sortBamFiles
)

ids_file = '../data/commonData/ids_data_p.csv'
working_folder = '../data/data_p/'
raw_folder = '../raw_data_p'
working_folder_name = 'data_p'
bowtie2mode = '--sensitive'

with open(ids_file, 'r') as samplesOntology:
    idsDf = pd.read_csv(samplesOntology, names=['id', 'tf', 'mut'])

with cd(working_folder):
    for index, id in idsDf.iterrows():
        gzs = []
        targetFolder = os.path.join(id.tf, str(id.mut))
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
                        samfileexperiment = '{}{}.sam'.format(id.tf, str(id.mut))
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
                                '/home/joaquin/projects/methylation/data', working_folder_name, 'Input/{}'.format(id.mut)
                            )
                            performGEM(targetFolder, inputControlpath, working_folder_name)


