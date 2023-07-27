from cdmanager import cd
import os
from pathlib import Path
import pandas as pd
import shutil
from pathlib import Path

from utilpipeline import (
    checkMD5isCorrect,
    checkFastaQLenght,
    performTrimGalore,
    qualityCheckTrimGalore,
    performBowtie2,
    getBamAndDeleteSam,
    sortBamFiles,
    performGEM,
    renameGemFolders,
    performBigWigextraction,
    renameAndMoveBigWig
)

from constants import genomeIndex, gemIndex, genomeSizes, efective_size


Species = 'Arabidopsis thaliana'
ids_file = '/home/joaquin/projects/methylation/data/commonData/ids_dap_on_atac_tfs.csv'
working_folder = '/home/joaquin/projects/methylation/data/data_dap_on_atac_tfs'
raw_folder = '/home/joaquin/projects/methylation/data/AllRawData/raw_data_dap_on_atac_1'
working_folder_name = 'data_dap_on_atac_tfs'
BWFolder = os.path.join('/home/joaquin/projects/methylation/data/bigwigs',working_folder_name)
gemsFolder = os.path.join('/home/joaquin/projects/methylation/data/gemFiles',working_folder_name)

bowtie2mode = '--sensitive'

# make sure you are using the correct files for each species
print(f'''species name = {Species}
          genomeIndex =  {genomeIndex}
          gemIndex = {gemIndex}
          genomeSizes = {genomeSizes}
          efective_size = {efective_size}
          ''')


# create bigwig folder
Path(working_folder).mkdir(parents=True, exist_ok=True)
Path(BWFolder).mkdir(parents=True, exist_ok=True)
# createGEMsummaryFolder
Path(gemsFolder).mkdir(parents=True, exist_ok=True)

with open(ids_file, 'r') as samplesOntology:
    idsDf = pd.read_csv(samplesOntology, names=['rawindex', 'tf'])

with cd(working_folder):
    for index, attr in idsDf.iterrows():
        gzs = []
        targetFolder = os.path.join(attr.tf)
        Path(targetFolder).mkdir(parents=True, exist_ok=True)

        originalfolder = os.path.join(raw_folder, attr.rawindex)
        file_names = os.listdir(originalfolder)
        if len(file_names) >= 2:
            #  gz + MD5 in case of single-read or 2 gzs and MD5 in case of pair-ends, more if divided long files
            print('Checking MD5 from ' + attr.rawindex)
            if checkMD5isCorrect(originalfolder):
                print('Checking Fastaq lenghts from ' + attr.rawindex)
                if checkFastaQLenght(originalfolder):
                    for fileInside in file_names:
                        if 'gz' in fileInside:
                            gzs.append((fileInside))
                            originalFile = os.path.join(originalfolder, fileInside)
                            shutil.move(originalFile, targetFolder)

                    print('Doing Trim galore in ' + targetFolder + ' from ' + attr.rawindex)
                    performTrimGalore(targetFolder)
                    for file in gzs:
                        destinationFile = os.path.join(targetFolder, file)
                        shutil.move(destinationFile, originalfolder)
                    print('Trim galore finished,checking results...')
                    if qualityCheckTrimGalore(targetFolder):
                        samfileexperiment = '{}.sam'.format(attr.tf)
                        print('Doing Bowtie2 in ' + targetFolder + ' from ' + attr.rawindex)
                        performBowtie2(
                            targetFolder,
                            bowtie2mode,
                            samfileexperiment
                                        )

                    getBamAndDeleteSam(targetFolder)
                    sortBamFiles(targetFolder)
                    if attr.tf == 'Input':
                        print('this is an input file so dont do GEM!')
                    else:
                        inputControlpath = os.path.join(
                            '/home/joaquin/projects/methylation/data', working_folder_name, 'Input/'
                        )
                        performGEM(targetFolder, inputControlpath, working_folder_name)
                    performBigWigextraction(targetFolder)
                    renameAndMoveBigWig(targetFolder, BWFolder)

renameGemFolders(working_folder,gemsFolder)

