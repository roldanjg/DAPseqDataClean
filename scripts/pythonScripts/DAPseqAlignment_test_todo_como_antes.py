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
project_id = 'test_todo_como_antes'
ids_file = f'/home/joaquin/projects/methylation/data/commonData/ids_data_{project_id}.csv'
working_folder = f'/home/joaquin/projects/methylation/data/data_{project_id}/'
raw_folder = f'/home/joaquin/projects/methylation/data/AllRawData/raw_data_dobles'
working_folder_name = f'data_{project_id}'
BWFolder = os.path.join('/home/joaquin/projects/methylation/data/bigwigs/',working_folder_name)
gemsFolder = os.path.join('/home/joaquin/projects/methylation/data/gemFiles/',working_folder_name)

bowtie2mode = '--sensitive'

# make sure you are using the correct files for each species
print(f'''species name = {Species}
          genomeIndex =  {genomeIndex}
          gemIndex = {gemIndex}
          genomeSizes = {genomeSizes}''')

# create bigwig folder
Path(working_folder).mkdir(parents=True, exist_ok=True)
# create bigwig folder
Path(BWFolder).mkdir(parents=True, exist_ok=True)
# createGEMsummaryFolder
Path(gemsFolder).mkdir(parents=True, exist_ok=True)

with open(ids_file, 'r') as samplesOntology:
    idsDf = pd.read_csv(samplesOntology, names=['rawindex', 'tf', 'descr'])

with cd(working_folder):
    for index, attri in idsDf.iterrows():
        gzs = []
        targetFolder = os.path.join(str(attri.tf),str(attri.descr))
        Path(targetFolder).mkdir(parents=True, exist_ok=True)

        originalfolder = os.path.join(raw_folder, attri.rawindex)
        file_names = os.listdir(originalfolder)
        # if len(file_names) >= 2:
        #     #  gz + MD5 in case of single-read or 2 gzs and MD5 in case of pair-ends,
        #     #  more if divided long files
        #     print('Checking MD5 from ' + attri.rawindex)
        #     if checkMD5isCorrect(originalfolder):
        #         print('Checking Fastaq lenghts from ' + attri.rawindex)
        #         if checkFastaQLenght(originalfolder):
        #             if len(file_names) > 4:
        #                 print('fourfiles in folder',originalfolder)
        #                 set_names = set()
        #                 listadearchi = os.listdir(originalfolder)
        #                 for filefq in listadearchi:
        #                     if 'fq' in filefq:
        #                         set_names.add(filefq.split('.fq')[0][:-1])
        #                 list_names = list(set_names)
        #                 # print(len(list_names))
        #                 onemerge = f'{originalfolder}/{list_names[0]}1.fq.gz {originalfolder}/{list_names[1]}1.fq.gz'
        #                 twomerge = f'{originalfolder}/{list_names[0]}2.fq.gz {originalfolder}/{list_names[1]}2.fq.gz'
        #                 base_file = os.path.join(working_folder,targetFolder,attri.rawindex)
        #                 mergereads = subprocess.run(f'cat {onemerge} > {base_file}_1.fq.gz && cat {twomerge} > {base_file}_2.fq.gz', shell=True, capture_output=True)
        #                 print(f'cat {onemerge} > {base_file}_1.fastq.gz && cat {twomerge} > {base_file}_2.fastq.gz')
        #                 print(mergereads.stdout, mergereads.stderr)
        #                 print('Doing Trim galore in ' + targetFolder + ' from ' + attri.rawindex)
        #                 performTrimGalore(targetFolder)
        #                 descompr = subprocess.run(f'rm {base_file}_1.fq.gz', shell=True,capture_output=True)
        #                 print(descompr.stdout,descompr.stderr)
        #                 descompr = subprocess.run(f'rm {base_file}_2.fq.gz', shell=True,capture_output=True)
        #                 print(descompr.stdout,descompr.stderr)
        #             else:
        #                 #  gz + MD5 in case of single-read or 2 gzs and MD5 in case of pair-ends,
        #                 #  more if divided long files
        #                 for fileInside in file_names:
        #                     if 'gz' in fileInside:
        #                         gzs.append((fileInside))
        #                         originalFile = os.path.join(originalfolder, fileInside)
        #                         shutil.move(originalFile, targetFolder)
        #                 print('Doing Trim galore in ' + targetFolder + ' from ' + attri.rawindex)
        #                 performTrimGalore(targetFolder)
        #                 for file in gzs:
        #                     destinationFile = os.path.join(targetFolder, file)
        #                     shutil.move(destinationFile, originalfolder)
        #             print('Trim galore finished,checking results...')
        #             if qualityCheckTrimGalore(targetFolder):
        #                 samfileexperiment = \
        #                 f'{str(attri.tf)}{str(attri.descr)}.sam'

        #                 print('Doing Bowtie2 in ' + targetFolder + ' from ' + attri.rawindex)
        #                 performBowtie2(
        #                     targetFolder,
        #                     bowtie2mode,
        #                     samfileexperiment
        #                                 )

        #             getBamAndDeleteSam(targetFolder)
        #             sortBamFiles(targetFolder)
        if attri.tf == 'Input':
            print('this is an input file so dont do GEM!')
        else:
            inputControlpath = os.path.join(
                '/home/joaquin/projects/methylation/data', working_folder_name, 'Input', 'Input'
            )
            performGEM(targetFolder, inputControlpath, working_folder_name)
#         performBigWigextraction(targetFolder)
#         renameAndMoveBigWig(targetFolder, BWFolder)
# renameGemFolders(working_folder,gemsFolder)
