import os
from pathlib import Path
import subprocess
import pandas as pd
from cdmanager import cd
from utilpipeline import (
    checkFastaQLenght, checkMD5isCorrect,
    getBamAndDeleteSam, performBigWigextraction,
    performBowtie2, performTrimGalore,
    qualityCheckTrimGalore, renameAndMoveBigWig,
    renameGemFolders, sortBamFiles,performGEM
                          )
import shutil
from constants import genomeIndex, gemIndex, genomeSizes


Species = 'Arabidopsis thaliana'
ids_file = '/home/joaquin/projects/methylation/data/commonData/ids_dap_on_atac_1.csv'
working_folder = '/home/joaquin/projects/methylation/data/data_dap_on_atac_1'
raw_folder = '/home/joaquin/projects/methylation/data/AllRawData/raw_data_dap_on_atac_1'
working_folder_name = 'data_dap_on_atac_1'
BWFolder = os.path.join('/home/joaquin/projects/methylation/data/bigwigs/',working_folder_name)
gemsFolder = os.path.join('/home/joaquin/projects/methylation/data/gemFiles/',working_folder_name)

bowtie2mode = '--sensitive'

# make sure you are using the correct files for each species
print(f'''species name = {Species}
          genomeIndex =  {genomeIndex}
          gemIndex = {gemIndex}
          genomeSizes = {genomeSizes}''')


# create bigwig folder
Path(BWFolder).mkdir(parents=True, exist_ok=True)
# createGEMsummaryFolder
Path(gemsFolder).mkdir(parents=True, exist_ok=True)

with open(ids_file, 'r') as samplesOntology:
    idsDf = pd.read_csv(samplesOntology, names=['rawindex', 'tf', 'treatment', 'rep'])

with cd(working_folder):
    for index, attri in idsDf.iterrows():
        gzs = []
        targetFolder = os.path.join(str(attri.tf),str(attri.treatment),str(attri.rep))
        Path(targetFolder).mkdir(parents=True, exist_ok=True)

        originalfolder = os.path.join(raw_folder, attri.rawindex)
        file_names = os.listdir(originalfolder)
        if len(file_names) >= 2:
            #  gz + MD5 in case of single-read or 2 gzs and MD5 in case of pair-ends,
            #  more if divided long files
            print('Checking MD5 from ' + attri.rawindex)
            if checkMD5isCorrect(originalfolder):
                print('Checking Fastaq lenghts from ' + attri.rawindex)
                if checkFastaQLenght(originalfolder):
                    for fileInside in file_names:
                        if 'gz' in fileInside:
                            gzs.append((fileInside))
                            originalFile = os.path.join(originalfolder, fileInside)
                            shutil.move(originalFile, targetFolder)

                    print('Doing Trim galore in ' + targetFolder + ' from ' + attri.rawindex)
                    performTrimGalore(targetFolder)
                    for file in gzs:
                        destinationFile = os.path.join(targetFolder, file)
                        shutil.move(destinationFile, originalfolder)
                    print('Trim galore finished,checking results...')
                    if qualityCheckTrimGalore(targetFolder):
                        samfileexperiment = \
                        f'{str(attri.tf)}{str(attri.treatment)}{str(attri.rep)}.sam'

                        print('Doing Bowtie2 in ' + targetFolder + ' from ' + attri.rawindex)
                        performBowtie2(
                            targetFolder,
                            bowtie2mode,
                            samfileexperiment
                                        )

                    getBamAndDeleteSam(targetFolder)
                    sortBamFiles(targetFolder)
                    if attri.tf == 'Input':
                        print('this is an input file so dont do GEM!')
                    else:
                        inputControlpath = os.path.join(
                            '/home/joaquin/projects/methylation/data', working_folder_name, 'Input',
                            str(attri.treatment), str(attri.rep)
                        )
                        performGEM(targetFolder, inputControlpath, working_folder_name)
                    performBigWigextraction(targetFolder)
                    renameAndMoveBigWig(targetFolder, BWFolder)


renameGemFolders(working_folder,gemsFolder)
