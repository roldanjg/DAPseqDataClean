from cdmanager import cd
import os
from pathlib import Path
import pandas as pd
import shutil
import subprocess
from utilpipeline import (
    checkMD5isCorrect,
    checkFastaQLenght,
    performTrimGaloreFourFiles,
    qualityCheckTrimGaloreFourFiles,
    performBismark

)

ids_file = '../data/commonData/ids_bisulfite_rep1_rep2.csv'
working_folder = '../data/bisulfite_rep1_rep2/'
raw_folder = '../raw_bisulfite_rep1_rep2'
working_folder_name = 'bisulfite_rep1_rep2'


with open(ids_file, 'r') as samplesOntology:
    idsDf = pd.read_csv(samplesOntology, names=['id', 'rep', 'time', 'tratement'])



with cd(working_folder):
    for index, id in idsDf.iterrows():
        gzs = []
        targetFolder = os.path.join(id.tf, str(id.rep), str(id.time), id.tratement)
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
                    performTrimGaloreFourFiles(targetFolder)
                    for file in gzs:
                        destinationFile = os.path.join(targetFolder, file)
                        shutil.move(destinationFile, originalfolder)
                    print('Trim galore finished,checking results...')
                    if qualityCheckTrimGaloreFourFiles(targetFolder):
                        print('Doing bismark in ' + targetFolder + ' from ' + id.id)
                        performBismark(targetFolder)

#                        getBamAndDeleteSam(targetFolder)
#                        if id.tf == 'Input':
#                            print('this is an input file so dont do GEM!')
#                        else:
#                            performGEM(targetFolder, f'{id.time}/{id.tratement}', working_folder_name)
#
