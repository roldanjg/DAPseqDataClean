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
    performGEM
)


with open('../data/commonData/ids_data_metilation.csv', 'r') as samplesOntology:
    idsDf = pd.read_csv(samplesOntology, names=['id', 'tf', 'type', 'time', 'tratement'])

with cd('../data/tfs/'):
    for index, id in idsDf.iterrows():

        targetFolder = os.path.join(id.tf, str(id.type), str(id.time), id.tratement)
        Path(targetFolder).mkdir(parents=True, exist_ok=True)

        originalfolder = os.path.join('../raw_data', id.id)
        file_names = os.listdir(originalfolder)
        if len(file_names) >= 2:
            #  gz + MD5 in case of single-read or 2 gzs and MD5 in case of pair-ends, more if divided long files
            print('Checking MD5 from ' + id.id)
            if checkMD5isCorrect(originalfolder):
                print('Checking Fastaq lenghts from ' + id.id)
                if checkFastaQLenght(originalfolder):
                    for fileInside in file_names:
                        if 'gz' in fileInside:
                            originalFile = os.path.join(originalfolder, fileInside)
                            shutil.move(originalFile, targetFolder)

                    print('Doing Trim galore in ' + targetFolder + ' from ' + id.id)
                    performTrimGalore(targetFolder)
                    print('Trim galore finished,checking results...')
                    if qualityCheckTrimGalore(targetFolder):
                        samfileexperiment = '{}{}{}{}.sam'.format(id.tf, str(id.type), str(id.time), id.tratement)
                        print('Doing Bowtie2 in ' + targetFolder + ' from ' + id.id)
                        performBowtie2(
                            targetFolder,
                            samfileexperiment
                                       )
                        getBamAndDeleteSam(targetFolder)
                        if id.tf == 'Input':
                            print('this is an input file so dont do GEM!')
                        else:
                            performGEM(targetFolder, f'{id.time}/{id.tratement}')
