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
from constants import genomeIndex, gemIndex, genomeSizes, efective_size


Species = 'Solanum tuberosum'
ids_file = '/home/joaquin/projects/methylation/data/commonData/ids_data_potato_salome_2.csv'
working_folder = '/home/joaquin/projects/methylation/data/data_potato_salome_2'
raw_folder = '/home/joaquin/projects/methylation/data/AllRawData/raw_data_potato_salome_2/raw_data'
working_folder_name = 'data_potato_salome_2'
BWFolder = os.path.join('/home/joaquin/projects/methylation/data/bigwigs_potato_salome_2',working_folder_name)
gemsFolder = os.path.join('/home/joaquin/projects/methylation/data/gemFiles_potato_salome_2',working_folder_name)

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
    idsDf = pd.read_csv(samplesOntology, names=['rawindex', 'tf','replicatenumber'])
    
with cd(working_folder):
    for index, attri in idsDf.iterrows():
        gzs = []
        targetFolder = os.path.join(attri.tf,str(attri.replicatenumber))
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
                    if len(file_names) > 4:
                        print('fourfiles in folder',originalfolder)
                        set_names = set()
                        listadearchi = os.listdir(originalfolder)
                        for filefq in listadearchi:
                            if 'fq' in filefq:
                                set_names.add(filefq.split('.fq')[0][:-1])
                        list_names = list(set_names)
                        # print(len(list_names))
                        onemerge = f'{originalfolder}/{list_names[0]}1.fq.gz {originalfolder}/{list_names[1]}1.fq.gz'
                        twomerge = f'{originalfolder}/{list_names[0]}2.fq.gz {originalfolder}/{list_names[1]}2.fq.gz'
                        base_file = os.path.join(working_folder,targetFolder,attri.rawindex)
                        mergereads = subprocess.run(f'cat {onemerge} > {base_file}_1.fq.gz && cat {twomerge} > {base_file}_2.fq.gz', shell=True, capture_output=True)
                        print(f'cat {onemerge} > {base_file}_1.fastq.gz && cat {twomerge} > {base_file}_2.fastq.gz')
                        print(mergereads.stdout, mergereads.stderr)
                        performTrimGalore(targetFolder)
                        descompr = subprocess.run(f'rm {base_file}_1.fq.gz', shell=True,capture_output=True)
                        print(descompr.stdout,descompr.stderr)
                        descompr = subprocess.run(f'rm {base_file}_2.fq.gz', shell=True,capture_output=True)
                        print(descompr.stdout,descompr.stderr)

   
                    print('Trim galore finished,checking results...')
                    if qualityCheckTrimGalore(targetFolder):
                        samfileexperiment = \
                        f'{attri.tf}{str(attri.replicatenumber)}.sam'

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
                            '/home/joaquin/projects/methylation/data', working_folder_name,
                            'Input', 'Input'
                        )
                        performGEM(targetFolder, inputControlpath, working_folder_name)
        performBigWigextraction(targetFolder)
        renameAndMoveBigWig(targetFolder, BWFolder)


renameGemFolders(working_folder,gemsFolder)